import configparser
import sys

from jiangsu.sql.taskdao import *


def init_status(pid, status, taskid):
    """
    此方法用于首次启动爬虫任务时，在数据库初始化爬虫状态
    :param pid: 进程号
    :param status: 状态值，其中0位停止，1为正在运行
    :param taskid: 任务id
    :return:
    """
    session = DBSession()
    taskstatus = TaskStatus()
    taskstatus.taskid = taskid
    taskstatus.pid = pid
    taskstatus.status = status
    session.add(taskstatus)
    session.commit()
    session.close()


def update_status_pid(pid, status, taskid):
    """
    如果此任务之前已经存在，调用此方法可修改爬虫的pid与状态
    :param pid:要修改的pid
    :param status:要修改的状态值
    :param taskid:被修改任务的任务id
    :return:
    """
    session = DBSession()
    t = session.query(TaskStatus).filter(TaskStatus.taskid == taskid).first()
    t.status = status
    t.pid = pid
    session.commit()
    session.close()


def update_status(status, taskid):
    """
    任务运行中，调用此方法修改爬虫状态
    :param pid:要修改的pid
    :param status:要修改的状态值
    :param taskid:被修改任务的任务id
    :return:
    """
    session = DBSession()
    t = session.query(TaskStatus).filter(TaskStatus.taskid == taskid).first()
    t.status = status
    session.commit()
    session.close()


def get_taskinfo(taskid):
    """
    根据任务id获取任务详情
    :param taskid:任务id
    :return: 返回此任务信息实例
    """
    session = DBSession()
    t = session.query(TaskInfo).filter(TaskInfo.id == taskid).first()
    return t


def get_taskstatus(taskid):
    """
    根据任务id获取此任务的状态
    :param taskid: 任务id
    :return: 任务状态实例
    """
    session = DBSession()
    t = session.query(TaskStatus).filter(TaskStatus.taskid == taskid).first()
    return t


def writeconf(taskid):
    """
    根据任务id获取数据库中配置信息，将其写到本地
    :param taskid:任务id
    :return:
    """
    session = DBSession()
    taskinfo = session.query(TaskInfo).filter(TaskInfo.id == taskid).first()
    user = session.query(User).filter(User.id == 20).first()
    guizeFile = open(sys.path[1] + "\\jiangsu\\conf\\rule\\" + taskinfo.rulename, 'w', encoding='utf-8')
    guizeFile.write(taskinfo.rulecontent)
    guizeFile.close()
    conf = configparser.ConfigParser()
    conf.add_section("rule")
    conf.add_section("info")
    conf.set("info", "taskid", str(taskinfo.id))
    conf.set("rule", 'rulename', taskinfo.rulename)
    conf.set("info", "hostname", taskinfo.hostname)
    conf.set("info", "taskname", taskinfo.taskname)
    conf.set("info", "url", taskinfo.url)
    conf.set("info", "uuid", taskinfo.uuid)
    conf.set("info", "user", user.username)
    with open(sys.path[1] + "\\jiangsu\\conf\\task.ini", 'w') as fw:
        conf.write(fw)


if __name__ == '__main__':
    writeconf(1)
