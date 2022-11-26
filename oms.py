import statistics
import uuid

class OrderManagementSystem():
  def __init__(self, in_progress_orders_capacity):
    self.capacity = in_progress_orders_capacity
    # Instead of deriving from the orders list I keep track here as this is faster
    self.num_of_orders_in_progress = 0
    self.orders = []
    self.delivery_times = []
  # Create an order: generates id, sets status to "in progress", taking creation_time, validate inputs
  def create_order(self, creation_time_stamp):
    # Validate creation_time
    if creation_time_stamp < 0:
      raise Exception("Invalid creation_time")
    # Check there is capacity for more orders
    if self.num_of_orders_in_progress >= self.capacity:
      raise Exception("Out of capacity")
    # Generate id
    id = uuid.uuid1()
    # Set status
    status = "in_progress"
    # Add order to list of orders
    self.orders.append({"id": id, "status": status, "creation_time_stamp": creation_time_stamp})
    # Increase num_of_orders_in_progress
    self.num_of_orders_in_progress += 1
    return id
  # Cancel an order: validate inputs, set status to "cancelled"
  def mark_order_cancelled(self, id):
    # Check id exists and throw exception if it doesn't exist
    matched_order = next(filter(lambda order: order.get('id') == id, self.orders), None)
    if matched_order == None:
      raise Exception("Invalid ID")
    if matched_order.get('status') != "in_progress":
      raise Exception("Order cannot be cancelled")
    # Set status to "cancelled"
    status = "cancelled"
    matched_order.update({"status": status})
    # Decrease num_of_orders_in_progress
    self.num_of_orders_in_progress -= 1
  # Deliver an order: validate inputs, set status to "delivered"
  def mark_order_delivered(self, id, delivery_time_stamp):
    # Check id exists and throw exception if not
    matched_order = next(filter(lambda order: order.get('id') == id, self.orders), None)
    if matched_order == None:
      raise Exception("Invalid ID")
    if matched_order.get('status') != "in_progress":
      raise Exception("Order cannot be delivered")
    # Set status to "delivered"
    status = "delivered"
    matched_order.update({"status": status})
    # Decrease num_of_orders_in_progress
    self.num_of_orders_in_progress -= 1
    # Retrieve delivery_time-stamp and creation_time_stamp
    creation_time_stamp = matched_order['creation_time_stamp']
    # Calculate delivery_time and add to list of delivery times
    delivery_time = delivery_time_stamp - creation_time_stamp
    self.delivery_times.append(delivery_time)

  def get_num_orders_in_progress(self):
    return self.num_of_orders_in_progress  
  
  def get_average_delivery_time(self):
    # Used statistics module to calculate mean of delivery times
    avg_delivery_time = statistics.mean(self.delivery_times)
    return avg_delivery_time

# Test cases
# Missing test case for invalid id
def invalid_creation_time():
  try:
    oms = OrderManagementSystem(5)
    first_order_id = oms.create_order(creation_time_stamp=-1)  
  except Exception as e:
    assert str(e) == "Invalid creation_time"
    
def out_of_capacity():
  try:
    oms = OrderManagementSystem(5)
    first_order_id = oms.create_order(creation_time_stamp=0.0)
    second_order_id = oms.create_order(creation_time_stamp=1.0)
    third_order_id = oms.create_order(creation_time_stamp=2.0)
    fourth_order_id = oms.create_order(creation_time_stamp=3.0)
    fifth_order_id = oms.create_order(creation_time_stamp=4.0)
    sixth_order_id = oms.create_order(creation_time_stamp=5.0)
  except Exception as e:
    assert str(e) == "Out of capacity"

def double_marking_as_cancelled():
  try:
    oms = OrderManagementSystem(5)
    first_order_id = oms.create_order(creation_time_stamp=0.0)
    oms.mark_order_cancelled(first_order_id)
    oms.mark_order_cancelled(first_order_id)
  except Exception as e:
    assert str(e) == "Order cannot be cancelled"

def double_marking_as_delivered():
  try:
    oms = OrderManagementSystem(5)
    first_order_id = oms.create_order(creation_time_stamp=0.0)
    oms.mark_order_delivered(first_order_id, delivery_time_stamp=2.5)
    oms.mark_order_delivered(first_order_id, delivery_time_stamp=2.5)
  except Exception as e:
    assert str(e) == "Order cannot be delivered"

def within_capacity():
  oms = OrderManagementSystem(5)
  first_order_id = oms.create_order(creation_time_stamp=0.0)
  second_order_id = oms.create_order(creation_time_stamp=1.0)
  third_order_id = oms.create_order(creation_time_stamp=2.0)
  fourth_order_id = oms.create_order(creation_time_stamp=3.0)
  fifth_order_id = oms.create_order(creation_time_stamp=4.0)
  oms.mark_order_cancelled(first_order_id)
  oms.mark_order_delivered(second_order_id, delivery_time_stamp=2.5)
  sixth_order_id = oms.create_order(5.0)
  assert oms.capacity == 5

def return_in_progress_and_avg_delivery_time():
  oms = OrderManagementSystem(5)
  first_order_id = oms.create_order(creation_time_stamp=0.0)
  second_order_id = oms.create_order(creation_time_stamp=1.0)
  oms.mark_order_cancelled(first_order_id)
  oms.mark_order_delivered(second_order_id, delivery_time_stamp=4.5)  
  third_order_id = oms.create_order(creation_time_stamp=2.0)
  fourth_order_id = oms.create_order(creation_time_stamp=3.0)
  oms.mark_order_cancelled(fourth_order_id)
  oms.mark_order_delivered(third_order_id, delivery_time_stamp=4.5)
  fifth_order_id = oms.create_order(creation_time_stamp=4.0)
  sixth_order_id = oms.create_order(creation_time_stamp=5.0)
  seventh_order_id = oms.create_order(creation_time_stamp=6.0)
  assert oms.get_num_orders_in_progress() == 3 # This should return 3
  assert oms.get_average_delivery_time() == 3.0 # This should return (3.5+2.5)/2 = 3.0

within_capacity()
return_in_progress_and_avg_delivery_time()
out_of_capacity()
invalid_creation_time()
double_marking_as_cancelled()
double_marking_as_delivered()