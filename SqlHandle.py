# -*- coding: utf-8 -*-
"""
Created on Wed May 16 20:46:31 2018

@author: Administrator
"""


from abc import ABCMeta, abstractmethod
class  SqlHandle:

    __metaclass__ = ABCMeta

    @abstractmethod
    def fetchall(self,sql):
        self.cursor.execute(sql)
        self.db.commit()
        return (self.cursor.fetchall()) 
    def fetchone(self,sql):
        self.cursor.execute(sql)
        self.db.commit()
        return (self.cursor.fetchone())

   
    