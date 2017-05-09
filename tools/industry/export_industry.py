#!/usr/bin/python
# -*- coding: utf-8 -*-
import xlwt

from mysql import query, query_one, save


def handle_data():
    data = []
    level_one_data = query(sql=u"SELECT * FROM industry WHERE level = 1 ORDER BY id DESC")
    for level_one in level_one_data:
        level_one_name = level_one.get("name")
        level_one_id = level_one.get("id")

        level_two_data = query(sql=u"SELECT * FROM industry WHERE parent_id = %s", list1=(level_one_id, ))
        for level_two in level_two_data:
            level_two_name = level_two.get("name")
            level_two_id = level_two.get("id")

            level_three_data = query(sql=u"SELECT * FROM industry WHERE parent_id = %s", list1=(level_two_id, ))
            
            if level_three_data == ():
                data.append((level_one_name, level_two_name, "", "", ""))
            else:
                for level_three in level_three_data:
                    level_three_name = level_three.get("name")
                    level_three_id = level_three.get("id")

                    level_four_data = query(sql=u"SELECT * FROM industry WHERE parent_id = %s", list1=(level_three_id, ))
                    
                    if level_four_data == ():
                        data.append((level_one_name, level_two_name, level_three_name, "", ""))
                    else:
                        for level_four in level_four_data:
                            level_four_name = level_four.get("name")
                            level_four_id = level_four.get("id")

                            level_five_data = query(sql=u"SELECT * FROM industry WHERE parent_id = %s", list1=(level_four_id, ))
                            
                            if level_five_data == ():
                                data.append((level_one_name, level_two_name, level_three_name, level_four_name, ""))
                            else:
                                for level_five in level_five_data:
                                    level_five_name = level_five.get("name")
                                    level_five_id = level_five.get("id")

                                    data.append((level_one_name, level_two_name, level_three_name, level_four_name, level_five_name))
                                              
    return data


def export(data):
    file = xlwt.Workbook()                # 注意这里的Workbook首字母是大写
    table = file.add_sheet('sheet_1', cell_overwrite_ok=True)

    for index, d in enumerate(data):
        table.write(index, 0, d[0])
        table.write(index, 1, d[1])
        table.write(index, 2, d[2])
        table.write(index, 3, d[3])

    # 保存文件
    file.save('/home/sdu/MyProject/tools/tools/industry/industry.xls')


def main():
    data = handle_data()
    export(data)



if __name__ == '__main__':
    main()
