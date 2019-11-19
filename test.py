import db
import util
import configparser

if __name__ == '__main__':
    conf_path = util.get_root_path() + "/conf/platform.conf"
    deploy_conf = configparser.ConfigParser()
    deploy_conf.read(conf_path)
    r = db.get_all_database(deploy_conf)
    print(r)