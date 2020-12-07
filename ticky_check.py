import operator
import re
import csv

#to get the count of Error and Info
def all_log(content):
    log_dict = {}
    log_list = ["ERROR", "INFO"]
    for item in log_list:
        for line in content:
            searched = re.findall(item, line)
            if len(searched)>0:
                if searched[0] == 'ERROR':
                    log_dict["ERROR"] = log_dict.get("ERROR",0)+1
                else:
                    log_dict["INFO"] = log_dict.get("INFO",0) + 1
    return  log_dict

#to get count of different error messages
def error_type(content):
    error_dict = {}
    for line in content:
        searched = re.findall(r"ticky: ERROR ([\w ']*) ", line)
        if len(searched)>0:
            item = searched[0]
            error_dict[item] = error_dict.get(item,0)+1
    return error_dict


def search_error(content):
    for line in content:
        searched = re.findall(r"ticky: ERROR ([\w ']*) ", line)
        name = re.findall(r"ticky: ERROR [\w ']* ([(\w .)]*)", line)
        if len(searched) > 0:
            pass
            #print(searched[0], name[0])

#Reading the content of files
def read_file(filename):
    file = open(filename)
    file_content = file.readlines()
    return file_content

#per user count of Error and Info
def per_user_error(content):
    user_dict = {}
    for line in content:
        if "ERROR" in line:
            name = re.findall(r"ticky: ERROR [\w ']* ([(\w .)]*)", line)
            if len(name) > 0:
                item = name[0]
                item = item.replace("(", "")
                item = item.replace(")", "")
                if item in user_dict:
                        user_dict[item]["ERROR"] += 1
                else:
                     user_dict[item] = {"ERROR": 1, "INFO": 0}
        if "INFO" in line:
            info_name = re.findall(r"ticky: INFO [\w ]*[\D]*[\d]*[\D] ([(\w .)]*)", line)
            if len(info_name) > 0:
                info_item = info_name[0]
                info_item = info_item.replace("(", "")
                info_item = info_item.replace(")", "")
                if info_item in user_dict:
                        user_dict[info_item]["INFO"] += 1
                else:
                     user_dict[info_item] = {"ERROR": 0, "INFO": 1}
    return user_dict

def to_csv(user_dict, error):
  print("Inside to csv")
  print(user_dict)
  with open("user_statistics.csv", "w") as users_csv:
    writer = csv.writer(users_csv)
    writer.writerow(["Username", "INFO", "ERROR"])
    for item, values in user_dict.items():
        for key in values:
            line = [item,values["INFO"],values["ERROR"]]
            print(line)
            writer.writerow(line)
            break
  with open("error_message.csv", "w") as error_csv:
    writer = csv.writer(error_csv)
    writer.writerow(["Error","Count"])
    writer.writerows(error)


if __name__ == '__main__':
    filename = "syslog.log"
    error_dict = dict()
    content = read_file(filename)

    #to get the count of Error and Info
    error_dict = all_log(content)

    #to get count of different error messages
    #error_dict_types = error_type(content)
    #print(error_dict_types)

    #to get the per user count of Error and Info
    user_dict = per_user_error(content)


    # Here, the dictionaries will be sorted
    user_dict = dict(sorted(user_dict.items()))
    error_dict = sorted(error_dict.items(), key=operator.itemgetter(1), reverse=True)


    #write to csv file
    to_csv(user_dict, error_dict)