# -*- coding: utf-8 -*-
import sys
import os
import socket
sys.path.append(os.path.join(os.path.dirname(__file__), "soaplib-2.0.0b2-py2.7.egg"))
from  soaplib.core import Application
from soaplib.core.service import DefinitionBase, soap
from soaplib.core.server.wsgi import Application as WSGIApp
from soaplib.core.model.primitive import Integer, String

import MySQLdb
from MySQLdb.cursors import DictCursor
from logger import get_logger
from lxml import etree
from contextlib import contextmanager

from tornado.wsgi import WSGIContainer
from tornado.httpserver import HTTPServer
from tornado.ioloop import IOLoop

log = get_logger()

class SOAPApp(Application):
    def parse_xml_string(self, xml_string, charset=None):
        try:
            if charset is None:
                raise ValueError(charset)
            root, xmlids = etree.XMLID(xml_string.decode(charset))
        except ValueError as e:
            root, xmlids = etree.XMLID(xml_string)
        return root, xmlids

class SoapServer(object):
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.soap_app = None
        self.wsgi_app = None

    def make_service(self, service_inst, tns="tns", name=None):
        if not isinstance(service_inst, list):
            service_inst = [service_inst]

        self.soap_app = SOAPApp(service_inst, tns, name)
        self.wsgi_app = WSGIApp(self.soap_app)

    def start_server(self):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        result = sock.connect_ex(("127.0.0.1", self.port))
        if result == 0:
            print "Port:", self.port, "in used"
            os._exit(2)
        container = WSGIContainer(self.wsgi_app)
        http_server = HTTPServer(container)
        http_server.listen(self.port, self.host)
        pid_file = os.path.join(os.path.dirname(sys.argv[0]), "server.pid")
        with open(pid_file, "w") as fd:
            fd.write(str(os.getpid()))
        IOLoop.current().start()

@contextmanager
def db_connect():
    conn = MySQLdb.connect(host="127.0.0.1", port=3320,
                           user="third_admin", passwd="eisoo.com",
                           db="third_party_infos", cursorclass=DictCursor,
                           charset="utf8")
    cursor = conn.cursor()
    yield cursor
    conn.commit()
    cursor.close()
    conn.close()

class OrgTask(object):
    deptId = ""
    deptName = ""
    deptFullName = ""
    deptType = ""
    superDeptId = ""
    gbm = ""
    level = ""
    isOrg = ""
    state = ""
    def __str__(self):
        content = """
        Orgtask:
            deptId=%s
            deptName=%s
            deptFullName=%s
            deptType=%s
            superDeptId=%s
            gbm=%s
            level=%s
            isOrg=%s
            state=%s
        """ % (self.deptId, self.deptName, self.deptFullName, self.deptType, self.superDeptId, self.gbm, self.level, self.isOrg, self.state)
        return content.encode("utf-8")

class UserTask(object):
    orclsequence = ""
    personuuid = ""
    password = ""
    state = ""
    deptcode = ""
    employeecode = ""
    officetel = ""
    mobile = ""
    email = ""
    specialties = ""
    personext2 = ""
    health = ""
    nativePlace = ""
    sex = ""
    deptId = ""
    stationName = ""
    isprimary = ""
    stationId = ""
    stationViewCode = ""
    idNum = ""
    cnname = ""
    personcode = ""

    def __str__(self):
        content = """
        Usertask:
            orclsequence=%s
            personuuid=%s
            password=%s
            state=%s
            deptcode=%s
            employeecode=%s
            officetel=%s
            mobile=%s
            email=%s
            specialties=%s
            personext2=%s
            health=%s
            nativePlace=%s
            sex=%s
            deptId=%s
            stationName=%s
            isprimary=%s
            stationId=%s
            stationViewCode=%s
            idNum=%s
            cnname=%s
            personcode=%s
        """ % (self.orclsequence, self.personcode, self.password, self.state, self.deptcode, self.employeecode,
               self.officetel, self.mobile, self.email, self.specialties, self.personext2, self.health, self.nativePlace,
               self.sex, self.deptId, self.stationName, self.isprimary, self.stationId, self.stationViewCode, self.idNum, self.cnname, self.personcode)
        return content.encode("utf-8")

class Analyzer(object):
    def org_task(self, org):
        with db_connect() as cursor:
            sql = "select * from t_third_departments where f_department_id=%s"
            cursor.execute(sql, org.deptId)
            result = cursor.fetchone()
            if not result:
                if org.opt == "add":
                    log.info(u"增加部门%s", org.deptId)
                    try:
                        sql = "insert into t_third_departments (f_department_id, f_name, f_parent_department_id) values (%s, %s, %s)"
                        cursor.execute(sql, (org.deptId, org.deptName, org.superDeptId))
                        log.info(u"增加部门成功%s", org.deptId)
                    except Exception as e:
                        log.error(e)
                        return e
                elif org.opt == "update":
                    log.error(u"更新部门失败，部门不存在%s", org.deptId)
                    return "Update error: dept %s not exist" % org.deptId
                elif org.opt == "delete":
                    log.error(u"删除部门失败，部门不存在%s", org.deptId)
                    return u"Delete error: dept %s not exist" % org.deptId
                else:
                    log.error(u"未知操作%s", org.deptId)
                    return "Option error: %s unkown opt" % org.deptId
            else:
                if org.opt == "add":
                    log.error(u"增加部门失败， 部门已存在%s", org.deptId)
                    return "Add error: dept %s exist" % org.deptId
                elif org.opt == "update":
                    log.info(u"更新部门%s", org.deptId)
                    try:
                        sql = "update t_third_departments set f_name=%s, f_parent_department_id=%s where f_department_id=%s"
                        cursor.execute(sql, (org.deptName, org.superDeptId, org.deptId))
                        log.info(u"更新部门成功%s", org.deptId)
                    except Exception as e:
                        log.error(e)
                        return e
                elif org.opt == "delete":
                    log.info(u"删除部门%s", org.deptId)
                    try:
                        sql = "delete from t_third_departments where f_department_id=%s"
                        cursor.execute(sql, org.deptId)
                        log.info(u"删除部门成功%s", org.deptId)
                    except Exception as e:
                        log.error(e)
                        return e
                else:
                    log.error(u"未知操作%s", org.deptId)
                    return "Option error: %s unkown opt" % org.deptId

    def user_task(self, user):
        with db_connect() as cursor:
            sql = "select * from t_third_users where f_user_id=%s"
            cursor.execute(sql, user.idNum)
            result = cursor.fetchone()
            if not result:
                if user.opt == "add":
                    log.info(u"增加用户%s", user.personcode)
                    try:
                        sql = "insert into t_third_users values (%s, %s, %s, %s, %s, %s, %s)"
                        cursor.execute(sql, (user.idNum, user.specialties, user.cnname, None, user.state, None, 999))
                        sql = "insert into t_third_user_department_relation (f_user_id, f_department_id) values (%s, %s)"
                        cursor.execute(sql, (user.idNum, user.deptcode))
                        log.info(u"增加用户成功%s", user.idNum)
                    except Exception as e:
                        log.error(e)
                        return e
                elif user.opt == "update":
                    log.error(u"更新用户失败，用户不存在%s", user.idNum)
                    return "Update error: user %s not exist" % user.idNum
                elif user.opt == "delete":
                    log.error(u"删除用户失败，用户不存在%s" % user.idNum)
                    return "Delete error: user %s not exist" % user.idNum
                else:
                    log.error(u"未知操作%s", user.idNum)
                    return "Option error: %s unkown opt" % user.idNum
            else:
                if user.opt == "add":
                    log.error(u"增加用户失败，用户已存在%s", user.idNum)
                    return "Add error: user %s exist" % user.idNum
                elif user.opt == "update":
                    log.info(u"更新用户")
                    try:
                        sql = "update t_third_users set f_login_name=%s, f_display_name=%s, f_status=%s where f_user_id=%s"
                        cursor.execute(sql, (user.specialties, user.cnname, user.state, user.idNum))
                        sql = "update t_third_user_department_relation set f_user_id=%s, f_department_id=%s"
                        cursor.execute(sql, (user.idNum, user.deptcode))
                        log.info(u"更新用户成功%s", user.idNum)
                    except Exception as e:
                        log.error(e)
                        return e
                elif user.opt == "delete":
                    log.info(u"删除用户")
                    try:
                        sql = "delete from t_third_users where f_user_id=%s"
                        cursor.execute(sql, user.idNum)
                        sql = "delete from t_third_user_department_relation where f_user_id=%s"
                        cursor.execute(sql, user.idNum)
                        log.info(u"删除用户成功%s", user.idNum)
                    except Exception as e:
                        log.error(e)
                        return e
                else:
                    log.error(u"未知操作%s", user.idNum)
                    return "Option error: %s unkown opt", user.idNum

    def _get_elm(self, node):
        for ch in node:
            if ch.text is None:
                continue
            if ch.tag == "stationUserInfoList":
                for sub_ch in ch[0]:
                    yield (sub_ch.tag, sub_ch.text.strip(""))
                continue
            yield (ch.tag, ch.text.strip(""))

    def _org_obj(self, dept):
        opt = dept.attrib["actionType"]
        org_ins = OrgTask()
        for (key, value) in self._get_elm(dept):
            setattr(org_ins, key, value)
        setattr(org_ins, "opt", opt)
        return self.org_task(org_ins)

    def _user_obj(self, user):
        opt = user.attrib["actionType"]
        user_ins = UserTask()
        for (key, value) in self._get_elm(user):
            setattr(user_ins, key, value)
        setattr(user_ins, "opt", opt)
        return self.user_task(user_ins)

    def parse_xml(self, xml_string):
        root = etree.XML(xml_string)
        if root.tag == "RLDeptInfo":
            return self._org_obj(root)
        if root.tag == "RLUserInfo":
            return self._user_obj(root)

ANALYZER = Analyzer()

class BaseService(DefinitionBase):
    @soap(String, String, _returns=String)
    def orgSync(self, servicecode, dataParas):
        if servicecode == "eisoozr":
            root = etree.XML(dataParas)
            ret = ANALYZER._org_obj(root)
            return ret

    @soap(String, String, _returns=String)
    def userSync(self, servicecode, dataParas):
        if servicecode == "eisoozr":
            root = etree.XML(dataParas)
            ret = ANALYZER._user_obj(root)
            return ret

if __name__ == "__main__":
    server = SoapServer("0.0.0.0", 8098)
    server.make_service(BaseService, "http://services.rbs.webservice.project.incon.com")
    log.info("Server satrt")
    server.start_server()
