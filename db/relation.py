# SubwayTraffic Platform
# Description: 
# File: relation
# Date: 2020/2/19 - 01:18

import db.engine


def init_relation():
    engine, cursor = db.engine.get_engine()
    sql = """
        create table if not exists entity_relation(
        id      bigint  auto_increment  primary key,
        uuid    char(27) not null,
        parent  char(27),
        child   char(27),
        relation varchar(30) not null
        ) charset utf8
    """
    cursor.execute(sql)
    engine.close()
    return


def add_relation(**kwargs):
    engine, cursor = db.engine.get_engine()
    sql = "insert into entity_relation(uuid, parent, child, relation) " \
          "values(%s, %s, %s, %s)"
    val = (kwargs["uuid"], kwargs["parent"], kwargs["child"], kwargs["relation"])
    cursor.execute(sql, val)
    engine.commit()
    engine.close()
    return


def pop_relation(entity_id):
    engine, cursor = db.engine.get_engine()
    sql = "delete from entity_relation where id='%s'" % entity_id
    cursor.execute(sql)
    engine.close()
    return


def delete_relation(uuid):
    engine, cursor = db.engine.get_engine()
    sql = "delete from entity_relation where uuid='%s'" % uuid
    cursor.execute(sql)
    engine.close()
    return


def search_relation(uuid):
    engine, cursor = db.engine.get_engine()
    sql = "select * from entity_relation where uuid='%s'" % uuid
    cursor.execute(sql)
    data = cursor.fetchall()
    relation_list = []
    for relation_data in data:
        each_relation = {}
        each_relation["id"] = relation_data[0]
        each_relation["uuid"] = relation_data[1]
        each_relation["parent"] = relation_data[2]
        each_relation["child"] = relation_data[3]
        each_relation["relation"] = relation_data[4]
        relation_list.append(each_relation)
    engine.close()
    return relation_list
