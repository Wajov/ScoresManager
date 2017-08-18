from django.http import HttpResponse
from django.shortcuts import render
import sqlite3


class student:
    def __init__(self, id, name, chinese, math, english, physics, chemistry):
        self.id = id
        self.name = name
        self.chinese = int(chinese)
        self.math = int(math)
        self.english = int(english)
        self.physics = int(physics)
        self.chemistry = int(chemistry)
        self.total = self.chinese + self.math + self.english + self.physics + self.chemistry


def add(request):
    content = {"warning" : ""}
    if request.POST:
        t = request.POST
        if t["id"] == "":
            content["warning"] = "请输入考号！"
        elif request.POST["name"] == "":
            content["warning"] = "请输入姓名！"
        elif t["chinese"] == "":
            content["warning"] = "请输入语文成绩！"
        elif t["math"] == "":
            content["warning"] = "请输入数学成绩！"
        elif t["english"] == "":
            content["warning"] = "请输入英语成绩！"
        elif t["physics"] == "":
            content["warning"] = "请输入物理成绩！"
        elif t["chemistry"] == "":
            content["warning"] = "请输入化学成绩！"
        else:
            total = int(t["chinese"]) + int(t["math"]) + int(t["english"]) + int(t["physics"]) + int(t["chemistry"])
            con = sqlite3.connect("db.sqlite3")
            cur = con.cursor()
            cur.execute("insert into students values('" + t["id"] + "', '" + t["name"] + "', " + t["chinese"] + ", " + t["math"] + ", " + t["english"] + ", " + t["physics"] + ", " + t["chemistry"] + ", " + str(total) + ")")
            cur.close()
            con.commit()
            con.close()
    return render(request, "add.html", content)


def rank(request):
    content = {"students": [], "warning" : ""}
    if request.POST:
        t = request.POST
        if "item" not in t:
            content["warning"] = "请选择用于排名的属性！"
        elif t["l"] == "":
            content["warning"] = "请输入下界！"
        elif t["r"] == "":
            content["warning"] = "请输入上界！"
        else:
            con = sqlite3.connect("db.sqlite3")
            cur = con.cursor()
            cur.execute("select * from students")
            for tmp in cur.fetchall():
                if t["item"] == "chinese":
                    temp = tmp[2]
                elif t["item"] == "math":
                    temp = tmp[3]
                elif t["item"] == "english":
                    temp = tmp[4]
                elif t["item"] == "physics":
                    temp = tmp[5]
                elif t["item"] == "chemistry":
                    temp = tmp[6]
                elif t["item"] == "total":
                    temp = tmp[7]
                if temp >= int(t["l"]) and temp <= int(t["r"]):
                    temp = student(tmp[0], tmp[1], tmp[2], tmp[3], tmp[4], tmp[5], tmp[6])
                    content["students"].append(temp)
            if t["item"] == "chinese":
                content["students"].sort(key = lambda x : x.chinese, reverse = True)
            elif t["item"] == "math":
                content["students"].sort(key = lambda x : x.math, reverse = True)
            elif t["item"] == "english":
                content["students"].sort(key = lambda x : x.english, reverse = True)
            elif t["item"] == "physics":
                content["students"].sort(key = lambda x : x.physics, reverse = True)
            elif t["item"] == "chemistry":
                content["students"].sort(key = lambda x : x.chemistry, reverse = True)
            elif t["item"] == "total":
                content["students"].sort(key = lambda x : x.total, reverse = True)
            cur.close()
            con.close()
    return render(request, "rank.html", content)


def query(request):
    content = {"students" : [], "warning" : ""}
    if request.POST:
        t = request.POST
        if "item" not in t:
            content["warning"] = "请选择用于查询的属性！"
        elif t["key"] == "":
            content["warning"] = "请输入关键字！"
        else:
            con = sqlite3.connect("db.sqlite3")
            cur = con.cursor()
            cur.execute("select * from students")
            for tmp in cur.fetchall():
                if t["item"] == "id":
                    temp = tmp[0]
                elif t["item"] == "name":
                    temp = tmp[1]
                if temp == t["key"]:
                    temp = student(tmp[0], tmp[1], tmp[2], tmp[3], tmp[4], tmp[5], tmp[6])
                    content["students"].append(temp)
            cur.close()
            con.close()
    return render(request, "query.html", content)


def delete(request):
    content = {"warning" : ""}
    if request.POST:
        t = request.POST
        if "item" not in t:
            content["warning"] = "请选择用于删除的属性！"
        elif t["key"] == "":
            content["warning"] = "请输入关键字！"
        else:
            con = sqlite3.connect("db.sqlite3")
            cur = con.cursor()
            if t["item"] == "id":
                cur.execute("delete from students where id = '" + t["key"] + "'")
            elif t["item"] == "name":
                cur.execute("delete from students where name = '" + t["key"] + "'")
            cur.close()
            con.commit()
            con.close()
    return render(request, "delete.html", content)


def modify(request):
    content = {"warning": ""}
    if request.POST:
        t = request.POST
        if "item" not in t:
            content["warning"] = "请选择用于修改的属性！"
        elif t["key"] == "":
            content["warning"] = "请输入关键字！"
        elif t["chinese"] == "":
            content["warning"] = "请输入修改后的语文成绩！"
        elif t["math"] == "":
            content["warning"] = "请输入修改后的数学成绩！"
        elif t["english"] == "":
            content["warning"] = "请输入修改后的英语成绩！"
        elif t["physics"] == "":
            content["warning"] = "请输入修改后的物理成绩！"
        elif t["chemistry"] == "":
            content["warning"] = "请输入修改后的化学成绩！"
        else:
            con = sqlite3.connect("db.sqlite3")
            cur = con.cursor()
            total = int(t["chinese"]) + int(t["math"]) + int(t["english"]) + int(t["physics"]) + int(t["chemistry"])
            if t["item"] == "id":
                cur.execute("update students set chinese = "+ t["chinese"] + " where id = '" + t["key"] + "'")
                cur.execute("update students set math = " + t["math"] + " where id = '" + t["key"] + "'")
                cur.execute("update students set english = " + t["chinese"] + " where id = '" + t["key"] + "'")
                cur.execute("update students set physics = " + t["physics"] + " where id = '" + t["key"] + "'")
                cur.execute("update students set chemistry = " + t["chemistry"] + " where id = '" + t["key"] + "'")
                cur.execute("update students set total = " + str(total) + " where id = '" + t["key"] + "'")
            elif t["item"] == "name":
                cur.execute("update students set chinese = " + t["chinese"] + " where name = '" + t["key"] + "'")
                cur.execute("update students set math = " + t["math"] + " where name = '" + t["key"] + "'")
                cur.execute("update students set english = " + t["chinese"] + " where name = '" + t["key"] + "'")
                cur.execute("update students set physics = " + t["physics"] + " where name = '" + t["key"] + "'")
                cur.execute("update students set chemistry = " + t["chemistry"] + " where name = '" + t["key"] + "'")
                cur.execute("update students set total = " + str(total) + " where name = '" + t["key"] + "'")
            cur.close()
            con.commit()
            con.close()
    return render(request, "modify.html", content)
