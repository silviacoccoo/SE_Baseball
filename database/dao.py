from database.DB_connect import DBConnect
from model.team import Team
class DAO:

    @staticmethod
    def get_teams_by_year(year):
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = """ 
        select distinct t.year,t.id, t.team_code, t.name
        from team t
        where t.year=%s
        """

        cursor.execute(query, (year,))

        for row in cursor:
            result.append(Team(**row))

        cursor.close()
        conn.close()
        return result # LISTA DI OGGETTI

    @staticmethod
    def get_years():
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = """ 
        select distinct team.year 
        from team 
        where team.year>=1980
        """

        cursor.execute(query)

        for row in cursor:
            result.append(int(row['year']))

        cursor.close()
        conn.close()
        return result  # LISTA DI ANNI - NUMERO INTERO

    @staticmethod
    def get_teams_salaries(year):
        conn = DBConnect.get_connection()

        result_id_map= {}
        cursor = conn.cursor(dictionary=True)
        query = """ 
                select s.year, s.team_id, sum(s.salary) as salario_tot
                from salary s 
                where s.year=%s
                group by s.year, s.team_id 
                """

        cursor.execute(query, (year,))

        for row in cursor:
            result_id_map[row['team_id']]=row['salario_tot']

        cursor.close()
        conn.close()
        return result_id_map # LISTA DI ANNI - NUMERO INTERO


