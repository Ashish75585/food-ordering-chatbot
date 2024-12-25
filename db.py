import pymysql

cnx = pymysql.connect(
            host='localhost',
            user='root',
            password='Styd3258',
            database='pandeyji_eatery'
        )


def get_next_order_id():
    cursor = cnx.cursor()

    # Executing the SQL query to get the next available order_id
    query = "SELECT MAX(order_id) FROM orders"
    cursor.execute(query)

    # Fetching the result
    result = cursor.fetchone()[0]

    #closing the cursor
    cursor.close()

    if result:
        return result + 1
    else:
        return 1


def insert_order_item(food_item, quantity, order_id):
    try:
        cursor = cnx.cursor()

        # Calling the stored procedure
        cursor.callproc('insert_order_item', (food_item, quantity, order_id))

        # commiting the changes
        cnx.commit()

        # closing the cursor
        cursor.close()

        print("order item inserted successfully")
        return 1
    except pymysql.MySQLError as e:
        print(f"Error: {e}")

        # Rollback changes if necessary
        cnx.rollback()

        return -1

    except Exception as e:
        print(f"An error occured: {e}")

        # Rollback changes if necessary
        cnx.rollback()

        return -1


def insert_order_tracking(order_id, status):
    cursor = cnx.cursor()

    # Inserting the record into order tracking table
    insert_query = "INSERT INTO order_tracking (order_id, status) VALUES (%s, %s)"
    cursor.execute(insert_query, (order_id, status))

    # committing the changes
    cnx.commit()

    # closing the cursor
    cursor.close()


def get_total_order_price(order_id):
    cursor = cnx.cursor()

    # Execute the SQL query to get the total order price
    query = f"SELECT get_total_order_price({order_id})" # "get_total_order_price() is a user defined function.
    cursor.execute(query)

    # Fetching the result
    result = cursor.fetchone()[0]

    # closing the cursor
    cursor.close()

    return result


def get_order_status(order_id: int):
    try:

        cursor = cnx.cursor()

        # Parameterized query
        query = "SELECT status FROM order_tracking WHERE order_id = %s"
        cursor.execute(query, (order_id,))
        result = cursor.fetchone()

        return result[0] if result else None

    except pymysql.MySQLError as e:
        print(f"Error: {e}")
        return None





value = get_order_status(41)
print(value)


if __name__ == "__main__":
    get_total_order_price(40)

