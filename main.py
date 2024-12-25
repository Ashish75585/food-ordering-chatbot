from flask import Flask, request, jsonify
import db
import generic_helper

app = Flask(__name__)

# this dictionary will store the temporary orders of the users until the user says "that's all I want".
# this is because the user may add or remove the order anytime.
inprogress_order = {}


@app.route("/", methods=["GET", "POST"])
def handle_request():
    # Retrieve the JSON data from the request
    payload = request.get_json()
    print(payload)
    # Extract the necessary information from the payload based on the structure of the WebhookRequest
    intent = payload['queryResult']['intent']['displayName']
    parameters = payload['queryResult']['parameters']
    output_contexts = payload['queryResult']['outputContexts']

    print(intent)
    #  session_id is required to keep track of user and there order, because there may be
    # thousands of people ordering at the same time.
    session_id = generic_helper.extract_session_id(output_contexts[0]['name'])

    intent_handler_dict = {
        'track.order - context: ongoing-tracking': track_order,
        'order.add - context: ongoing-order': add_to_order,
        'order.remove - context: ongoing-order': remove_from_order,
        'order.complete - context: ongoing-order': complete_order,
        'new.order': reset_inprogress_order_dict,
    }

    return intent_handler_dict[intent](parameters, session_id)


def reset_inprogress_order_dict(parameters: dict, session_id: str):
    inprogress_order.clear()
    return ""

# Step 1: locate the session id record
# Step 2: get the value from dict: {"vada pav": 3, "pizza": 2, "mango lassi": 1}
# Step 3: remove the food items.
# we will maintain a list that contains the food items to be removed.
def remove_from_order(parameters: dict, session_id: str):
    print("remove_from_order", inprogress_order)
    if session_id not in inprogress_order:
        return jsonify({
            "fulfillment_text": "I'm having a trouble finding your order. Sorry! Can you place anew order please?"
        })

    current_order = inprogress_order[session_id]
    food_items = parameters['food-item']

    removed_items = []  # keep track of removed items
    no_such_items = []  # keep track of items which are not in current_order.

    for item in food_items:
        if item not in current_order:
            no_such_items.append(item)
        else:
            removed_items.append(item)
            del current_order[item]

    if len(removed_items) > 0:
        fulfillment_text = f"Removed {','.join(removed_items)} from your order."

    if len(no_such_items) > 0:
        fulfillment_text = f'Your current order does not have {",".join(no_such_items)}'

    if len(current_order.keys()) == 0:
        fulfillment_text += "Your order is empty!"
    else:
        order_str = generic_helper.get_str_from_food_dict(current_order)
        fulfillment_text += f" Here is what's left in your order: {order_str}"

    return jsonify({"fulfillmentText": fulfillment_text})


def complete_order(parameters: dict, session_id: str):
    print("complete order", inprogress_order)
    if session_id not in inprogress_order:
        fulfillment_text = "I'm having a trouble finding your order. Sorry! Can you place anew order please?"
    else:
        order = inprogress_order[session_id]
        order_id = save_to_db(order)

        if order_id == -1:
            fulfillment_text = "Sorry, I couldn't process your order due to a backend error. " \
                               "Please place a new order again."
        else:
            order_total = db.get_total_order_price(order_id)
            fulfillment_text = f"Awesome! We have placed your order." \
                               f"Here is your order id # {order_id}." \
                               f"Your order total is {order_total} which you can pay at the time of delivery!"
        del inprogress_order[session_id]  # it will remove the session_id from the dict.
    return jsonify({"fulfillmentText": fulfillment_text})


def save_to_db(order: dict):  # order = {"pizza": 2, "chhole" 1}

    next_order_id = db.get_next_order_id()

    for food_item, quantity in order.items():
        rcode = db.insert_order_item(
            food_item,
            quantity,
            next_order_id
        )

        if rcode == -1:
            return -1
    db.insert_order_tracking(next_order_id, "in progress")
    return next_order_id


def add_to_order(parameters: dict, session_id: str):
    food_items = parameters["food-item"]
    quantities = parameters["number"]

    print("add to order", inprogress_order)

    if len(food_items) != len(quantities):
        fulfillment_text = "Sorry I didn't understand. Can you please specify food items and quantities clearly."
    else:
        # Create dictionary
        new_food_dict = dict(zip(food_items, quantities))

        if session_id in inprogress_order:  # go to line 148
            current_food_dict = inprogress_order[session_id]
            # merging the previous orders with new order
            current_food_dict.update(new_food_dict)
            inprogress_order[session_id] = current_food_dict
        else:
            inprogress_order[session_id] = new_food_dict

        order_str = generic_helper.get_str_from_food_dict(inprogress_order[session_id])
        fulfillment_text = f"So far you have: {order_str}. Do you need anything else?"

    return jsonify({"fulfillmentText": fulfillment_text})


def track_order(parameters: dict, session_id: str):
    order_id = int(parameters['order_id'])
    order_status = db.get_order_status(order_id)
    if order_status:
        fulfillment_text = f"The order status for order id: {order_id} is: {order_status}"
    else:
        fulfillment_text = f"No order with order id: {order_id}"

    return jsonify({"fulfillmentText": fulfillment_text})


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)


# if the user 1, with session_id = 1, has already ordered something (say 2 samosa and 1 pizza)
# inprogress_orders = {
#     'session_id_1': {samosa: 2, pizza: 1}
# }
# and after placing the order he wants to add more food_items in his order (say 3 mango lassi)
# new_order = {session_id_1: {mango lassi: 3}}
# then we need to merge the dictionaries with same session_id.

# If the session_id is not in inprogress_order, it means it's a fresh order.
# In that case we just push this session_id as a key and orders as value in inprogress_order.

