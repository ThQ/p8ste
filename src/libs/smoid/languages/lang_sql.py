from smoid.languages import Check, CheckCollection


class SqlCommandsCheck (Check):
    def __init__ (self):
        Check.__init__(self)
        self.name = "Sql:Commands"
        self.example = "create table sql_commands;"

        sql_commands = []
        #sql_commands.append("GROUP BY")
        #sql_commands.append("HAVING")
        #sql_commands.append("ORDER BY")
        #sql_commands.append("ALTER")
        sql_commands.append("CREATE TABLE")
        sql_commands.append("COMMIT")
        sql_commands.append("DELETE FROM")
        sql_commands.append("DROP")
        sql_commands.append("GRANT")
        sql_commands.append("INSERT INTO")
        sql_commands.append("MERGE")
        sql_commands.append("REVOKE")
        sql_commands.append("ROLLBACK")
        sql_commands.append("SELECT")
        sql_commands.append("TRUNCATE")
        sql_commands.append("UPDATE")

        re_commands = ""
        for command in sql_commands:
            if re_commands != "":
                re_commands += "|"
            re_commands += "(?:" + command + ")"
        re = "(^|;|\r|\n)\s*(" + re_commands + ")\s+"

        self.add_language("sql")
        self.add_multiple_matches(re, 20)


class SqlCheckCollection (CheckCollection):
    def __init__(self):

        self.name = "sql"

        self.append(SqlCommandsCheck())
