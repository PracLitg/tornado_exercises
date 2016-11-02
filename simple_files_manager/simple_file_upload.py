#!/usr/bin/python
#-*- encoding:utf-8 -*-
import tornado.httpserver
import tornado.options
import tornado.ioloop
import tornado.web
import shutil
import os
import time
import re
import urllib
import pymysql.cursors
from config_ope import DisposeConfigration
from tornado.web import HTTPError


class BaseHandler(tornado.web.RequestHandler):
    def get_current_user(self):
        return self.get_secure_cookie('username')


class LoginHandler(BaseHandler):
    def get(self):
        self.render('home_page.html')

    def post(self):
        username = self.get_argument('username')
        password = self.get_argument('password')
        with self.application.connection.cursor() as cursor:
            sql = "SELECT `password` FROM `users` WHERE `email`=%s"
            cursor.execute(sql,(username))
            result = cursor.fetchone()
            if result:
                if result['password'] == password:
                    self.set_secure_cookie('username', self.get_argument('username'))
                    self.redirect('/catalog')
            else:
                self.redirect('/login')


class GetCatalogHandler(BaseHandler):
    def get(self):
        path = self.request.path.rstrip('/')
        cur_files_path = self.get_cur_path(path)
        try:
            all_files_list = os.listdir(cur_files_path)
        except os.error:
            raise HTTPError(404, 'File Not Found')
        dir_list = []
        href_list = []
        for name in all_files_list:
            full_name = os.path.join(cur_files_path, name);
            href_list.append(path + '/' + name)
            if os.path.isdir(full_name):
                name += '/'
            dir_list.append(name)
        self.render('index.html', directory=dir_list, links=href_list)

    @tornado.web.authenticated
    def post(self):
        path = self.request.path.rstrip('/')
        cur_files_path = self.get_cur_path(path)
        file_metas = self.request.files['file']
        for meta in file_metas:
            # {"filename":...,"content_type":...,"body":...}
            filename = meta['filename']
            filepath = os.path.join(cur_files_path,filename)
            # some files need to be stored as binary
            with open(filepath,'wb') as up:
                up.write(meta['body'])
            self.redirect(path)

    def get_cur_path(self, path):
        dir_path = path.split('/',2)
        if len(dir_path) == 2:
            dst_path = ''
        else:
            dst_path = dir_path[2]
        cur_files_path = os.path.join('files', dst_path)
        return cur_files_path


class DownloadFileHandler(tornado.web.RequestHandler):
    def post(self):
        file_dir = 'files'
        print self.request.path
        file_name = self.request.path[15:]
        print file_name
        file_path = '%s/%s' % (file_dir, file_name)
        if not file_name or not os.path.exists(file_path):
            raise HTTPError(404)
        self.set_header('Content-Type', 'application/force-download')
        self.set_header('Content-Disposition', 'attachment; filename=%s' % file_name)
        with open(file_path, 'rb') as f:
            try:
                while True:
                    buffer_ = f.read(4096)
                    if buffer_:
                        self.write(buffer_)
                    else:
                        f.close()
                        self.finish()
                        return
            except:
                raise HTTPError(404)
        raise HTTPError(500)


class Application(tornado.web.Application):
    def __init__(self):
        handlers = [
            (r'/login',LoginHandler),
            (r'/file_download.*',DownloadFileHandler),
            (r'/catalog.*',GetCatalogHandler),
        ]

        settings = {
            'template_path':os.path.join(os.path.dirname(__file__), 'templates'),
            'static_path':os.path.join(os.path.dirname(__file__), 'static'),
            'cookie_secret':'Say Less But Do More',
            'xsrf_cookies':False,
            'login_url':'/login',
        }

        super(Application, self).__init__(handlers,**settings)

        self.connection = pymysql.connect(host='localhost',user='root',
            password='helloworld',db='firewall',cursorclass=pymysql.cursors.DictCursor)


if __name__ == '__main__':
    tornado.options.parse_command_line()
    app = tornado.httpserver.HTTPServer(Application())
    app.listen(8000)
    tornado.ioloop.IOLoop.instance().start()
