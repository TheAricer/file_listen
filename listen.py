#coding:utf-8
#Author by Arice@Molecule Labs

import time
import os
from io import BytesIO as StringIO
from apscheduler.schedulers.blocking import BlockingScheduler

class listen:
    def __init__(self,directory,s):
        self.directory = directory
        self.s = s

    def dict_constrast(self, file_dict_double, file_dict, f):
        NowTime = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
        file_dict_three = eval(f.getvalue())
        dict_key = file_dict_double.viewkeys() ^ file_dict_three.viewkeys()
        dict_value = file_dict_double.viewkeys() & file_dict_three.viewkeys()
        #文件增加/删除
        if len(dict_key) == 0:
            self.s.send(NowTime+ '--' + 'Is_Alive')
        else:
            for key in dict_key:
                for double in file_dict_double:
                    if key == double:
                        print NowTime+ '--' + 'Add/Change the file:'+ key + '\t'
                        val1 = NowTime+ '--' + 'Add/Change the file:'+ key + '\t'
                        self.s.send(val1)
                for three in file_dict_three:
                    if key == three:
                        print NowTime+ '--' + 'Del/Change the file:'+ key + '\t'
                        val2 = NowTime+ '--' + 'Del/Change the file:'+ key + '\t'
                        self.s.send(val2)
        #文件权限/大小/时间
        for value in dict_value:
            if file_dict_three[value] == file_dict_double[value]:
                pass
            elif file_dict_double[value]['Size'] == file_dict_three[value]['Size'] and file_dict_double[value]['Permissions'] == file_dict_three[value]['Permissions']:
                print NowTime + '--' + 'Change Time,Don\'t Change file Permissions And Size:'+ value + '--' + str(file_dict_double[value]) + '\t'
                val3 = NowTime + '--' + 'Change Time,Don\'t Change file Permissions And Size:'+ value + '--' + str(file_dict_double[value]) + '\t'
                self.s.send(val3)
            elif file_dict_double[value]['Size'] != file_dict_three[value]['Size']:
                print NowTime+ '--' + 'Change the file Size,Other results is:'+ value + '--' + str(file_dict_double[value]) + '\t'
                val4 = NowTime+ '--' + 'Change the file Size,Other results is:'+ value + '--' + str(file_dict_double[value]) + '\t'
                self.s.send(val4)
            elif file_dict_double[value]['Permissions'] != file_dict_three[value]['Permissions']:
                print NowTime + '--' + 'Change the file Permissions,Other results is:'+ value + '--' + str(file_dict_double[value]) + '\t'
                val5 = NowTime + '--' + 'Change the file Permissions,Other results is:'+ value + '--' + str(file_dict_double[value]) + '\t'
                self.s.send(val5)
            else:
                self.s.send(NowTime + '--' + 'Is_Alive')
        f.truncate(0)
        f.seek(0)
        f.write(str(file_dict_double))

    def dict_directory(self):
        dict_dir = {}
        for root,dirs,files in os.walk(self.directory):
            #文件属性存储
            for name in files:
                linshi = {}
                filepath = root + '/' + name
                CreateTime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(os.path.getctime(filepath)))
                AccessTime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(os.path.getatime(filepath)))
                ChangeTime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(os.path.getmtime(filepath)))
                Permissions = oct(os.stat(filepath).st_mode)[-3:]
                Size = os.path.getsize(filepath)
                linshi['CreateTime'], linshi['AccessTime'], linshi['ChangeTime'], linshi['Permissions'], linshi['Size'] = CreateTime, AccessTime, ChangeTime, Permissions, Size
                dict_dir[filepath] = linshi
        return dict_dir
                    

    def Start(self, file_dict, Tips, f):
        if len(Tips):
            file_dict_double = {}
            file_dict_double = self.dict_directory()
            self.dict_constrast(file_dict_double, file_dict, f)
        else:
            Tips.append('Tips')
            file_dict = self.dict_directory()
            f.write(str(file_dict))

    def Run(self):
        file_dict, Tips = {}, []
        f=StringIO()
        sched = BlockingScheduler()
        sched.add_job(self.Start,'interval',seconds = 10,args = [file_dict,Tips,f])
        sched.start()
