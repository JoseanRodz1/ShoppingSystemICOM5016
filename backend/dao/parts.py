from backend.config.pg import pg_config
import psycopg2


class PartDAO:
    def __init__(self):
        connection_url = "dbname =%s user=%s password=%s port =%s host=%s" \
                         % (pg_config['dbname'], pg_config['user'], pg_config['password'],
                            pg_config['dbport'], pg_config['host'])
        self.conn = psycopg2.connect(connection_url)

    """
        Select all records from Parts table.
    """

    def getAllParts(self):
        # query = "select tablename from pg_catalog.pg_Tables where tableowner != 'postgres'"
        query = "SELECT * from parts"
        cursor = self.conn.cursor()
        cursor.execute(query)

        result = []
        for row in cursor:
            result.append(row)
        return result

    """
        Select all parts record from Parts table where part_id equals id desired. 
    """

    def getPartById(self, part_id):
        query = "select * from parts where part_id = '%s'"
        cursor = self.conn.cursor()
        cursor.execute(query, (part_id,))
        result = cursor.fetchone()
        return result

    """
        Selects all parts from specified category.
    """

    def getPartbyCatname(self, cat_name):
        query = "select part_name,part_id, part_price, part_info, quantity from (parts natural inner join categories) where cat_name = %s"
        cursor = self.conn.cursor()
        cursor.execute(query, (cat_name,))
        result = []
        for row in cursor:
            result.append(row)
        return result

    """
        Selects parts less than or equal to desired price. Used to filter items.
    """

    def getPartsByPriceLessThanOrEqualTo(self, part_price):
        query = "select * from parts where part_price <= %s"
        cursor = self.conn.cursor()
        cursor.execute(query, (part_price,))
        result = []

        for row in cursor:
            result.append(row)
        return result

    """
        Selects all parts from Parts table and orders them alphabetically in ascending order (A-Z).
    """

    def order_parts_by_name(self):
        query = "select * from parts order by part_name"
        cursor = self.conn.cursor()
        cursor.execute(query)

        result = []
        for row in cursor:
            result.append(row)
        return result

    """
        Selects all parts from Parts table and orders them alphabetically in descending order (A-Z).
    """

    def order_parts_by_name_desc(self):
        query = "select * from parts order by part_name desc"
        cursor = self.conn.cursor()
        cursor.execute(query)

        result = []
        for row in cursor:
            result.append(row)
        return result

    """
        Select all parts ordered by their price in ascending order.
    """

    def order_parts_by_price(self):
        query = "select * from parts order by part_price"
        cursor = self.conn.cursor()
        cursor.execute(query)

        result = []
        for row in cursor:
            result.append(row)
        return result

    """
        Select all parts ordered by their price in ascending order.
    """

    def order_parts_by_price_desc(self):
        query = "select * from parts order by part_price desc"
        cursor = self.conn.cursor()
        cursor.execute(query)

        result = []
        for row in cursor:
            result.append(row)
        return result

    """
        Adds new part record to Parts table. Admin usage.
    """

    def newPart(self, part_name, part_price, cat_id, quantity, part_info):
        cursor = self.conn.cursor()
        query = "insert into parts (part_name, part_price, cat_id, quantity, part_info) values(%s, %s, %s, %s, " \
                "%s) returning part_id "
        cursor.execute(query, (part_name, part_price, cat_id, quantity, part_info,))
        part_id = cursor.fetchone()[0]
        self.conn.commit()
        return part_id

    """
        Admin usage. Updates parts  attributes of the part specified by given part id.
    """

    def updatePart(self, part_id,  part_price,  quantity):
        query = "update parts set part_price = %s,  quantity = %s where " \
                "part_id = %s; "
        cursor = self.conn.cursor()
        cursor.execute(query, ( part_price,  quantity, part_id))
        rowcount = cursor.rowcount
        self.conn.commit()
        return rowcount != 0

    """
            Admin usage. Delete part specified by given part id.
        """

    def deletePart(self, part_id):
        cursor = self.conn.cursor()
        prequery = "select part_id from wishlist where part_id = %s"
        cursor.execute(prequery, (part_id,))
        if cursor.rowcount !=0:
            wishlist = "delete from wishlist where part_id = %s"
            cursor.execute(wishlist, (part_id,))
            self.conn.commit()

        query = "delete from parts where part_id = %s;"
        cursor.execute(query, ([part_id]))
        self.conn.commit()
        return part_id



    def removeQuantity(self, part_id, bought):
        query = "update parts set quantity = (quantity - %s) where part_id = %s"
        cursor = self.conn.cursor()
        cursor.execute(query, (bought, part_id,))
        self.conn.commit()
        print("Quantity Removed for:",part_id, "Quantity = ", bought)
        return part_id
