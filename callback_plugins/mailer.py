""" Custom Ansible mailer callback plugin module. """
from __future__ import absolute_import, division, print_function
__metaclass__ = type  # pylint: disable=invalid-name
from email.message import EmailMessage
import smtplib
from pprint import pformat
from ansible.plugins.callback import CallbackBase


class CallbackModule(CallbackBase):
    """ Mail host admin when playbooks complete. """

    CALLBACK_VERSION = 2.0
    CALLBACK_TYPE = 'notification'
    CALLBACK_NAME = 'mailer'
    CALLBACK_NEEDS_WHITELIST = False

    _failures = []
    _play = None
    _tasks = {}  # Maps hosts to tasks / task status.

    def _email_admin(self, subject, body):
        """ Email host admin. """
        msg = EmailMessage()
        msg.set_content(body)
        play_vars = self._play.get_variable_manager().get_vars()
        msg['Subject'] = '[%s] %s' % (play_vars['hostname'], subject)
        msg['From'] = '<noreply@%s>' % play_vars['hostname']
        msg['To'] = '<%s>' % play_vars['admin_email']
        with smtplib.SMTP('localhost') as server:
            server.send_message(msg)

    def _update_tasks(self, task):
        """ Update the host-to-tasks dict. """
        hostvars = task.get_variable_manager().get_vars()['hostvars']
        for host, _ in hostvars.items():
            if not self._tasks.get(host):
                self._tasks[host] = []
            self._tasks[host].append([task, ""])

    # Callback overrides.

    def playbook_on_stats(self, stats):
        """ Process playbook stats event for each host. """

        # Set playbook status to complete or failed.
        status = 'complete'
        for host in stats.processed.keys():
            summary = stats.summarize(host)
            if summary['failures'] or summary['unreachable']:
                status = 'failed'
                break

        # Generate a per-host dict of tasks with non-empty status.
        tasklist = {}
        for host, tasks in self._tasks.items():
            tasklist[host] = []
            for task in tasks:
                if task[1]:
                    tasklist[host].append(task)

        # Format and send the admin email.
        body = 'Playbook tasks:\n\n%s' % pformat(tasklist)
        if self._failures:
            body += '\n\n%s' % '\n\n'.join(self._failures)
        self._email_admin('%s %s' % (self._play.name, status), body)

    def runner_on_failed(self, host, res, ignore_errors=False):
        """ Process failed task result. """

        # Set status for failed tasks.
        if self._tasks.get(host):
            self._tasks[host][-1][1] = 'failed'
        else:
            self._email_admin(
                'Missing host for failed task', '%s\n\n%s' % (host, res)
            )

        # Append the failure reason to the failures list.
        if res.get('stderr'):
            message = res['stderr']
        elif res.get('msg'):
            message = res['msg']
        elif res.get('failure'):
            message = res['failure']
        else:
            message = 'Unknown task failure reason.'
        self._failures.append('%s: %s' % (host, message))

    def runner_on_ok(self, host, res):
        """ Process ok task result. """

        # Set status for changed tasks, leave empty for others.
        if res.get('changed'):
            if self._tasks.get(host):
                self._tasks[host][-1][1] = 'changed'
            else:
                self._email_admin(
                    'Missing host for OK task', '%s\n\n%s' % (host, res)
                )

    def v2_playbook_on_play_start(self, play):
        """ Process playbook start events. """
        self._play = play

    def v2_playbook_on_handler_task_start(self, task):
        """ Process handler start events. """
        self._update_tasks(task)

    def v2_playbook_on_task_start(self, task, is_conditional):
        """ Process task start events. """
        self._update_tasks(task)
