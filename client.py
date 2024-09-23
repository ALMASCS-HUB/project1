import quickfix as fix
import quickfix44 as fix44
import random

class Client(fix.Application):
    def __init__(self):
        super().__init__()
        self.session_id = None
        self.order_statuses = {}

    def onCreate(self, session_id):
        self.session_id = session_id
        print(f"Session created - {session_id}")

    def onLogon(self, session_id):
        print(f"Logon successful for session {session_id}")

    def onLogout(self, session_id):
        print(f"Logout - {session_id}")

    def toAdmin(self, message, session_id):
        pass

    def fromAdmin(self, message, session_id):
        pass

    def toApp(self, message, session_id):
        print(f"Sending message: {message}")

    def fromApp(self, message, session_id):
        print(f"Received message: {message}")
        
        if message.getHeader().getField(fix.MsgType()) == fix.MsgType_ORDER_EXECUTION_REPORT:
            cl_ord_id = message.getField(fix.ClOrdID())
            status = message.getField(fix.OrdStatus())
            self.order_statuses[cl_ord_id] = status
            print(f"Order execution report received: {cl_ord_id} - Status={status}")

    def _place_order(self, side, symbol, quantity):
        if self.session_id is None:
            print("Cannot place order: session not established.")
            return None
        
        order = fix44.NewOrderSingle()
        order_id = gen_order_id()
        order.setField(fix.ClOrdID(order_id))
        order.setField(fix.Symbol(symbol))
        order.setField(fix.Side(side))
        order.setField(fix.OrderQty(quantity))
        order.setField(fix.OrdType(fix.OrdType_MARKET))
        order.setField(fix.TransactTime())

        fix.Session.sendToTarget(order, self.session_id)
        print(f"Order sent: Side={side}, Symbol={symbol}, Quantity={quantity}")
        return order_id

    def place_order(self, side, symbol, quantity):
        if side == 'buy':
            return self._place_order(fix.Side_BUY, symbol, quantity)
        elif side == 'sell':
            return self._place_order(fix.Side_SELL, symbol, quantity)
        else:
            print("Invalid order side. Must be 'buy' or 'sell'.")
            return None

    def get_order_status(self, cl_ord_id):
        return self.order_statuses.get(cl_ord_id, "Order status not found")

def gen_order_id():
    return str(random.randint(100000, 999999))

def start_terminal_input(client):
    while True:
        print("\nEnter order details (or type 'exit' to quit):")
        side = input("Side (buy/sell): ").strip().lower()
        if side == 'exit':
            break
        symbol = input("Symbol: ").strip()
        quantity = input("Quantity: ").strip()
        
        if not quantity.isdigit() or int(quantity) <= 0:
            print("Invalid quantity. Must be a positive integer.")
            continue
        
        order_id = client.place_order(side, symbol, int(quantity))
        if order_id:
            print(f"Order placed successfully. Order ID: {order_id}")
        else:
            print("Failed to place order.")

if __name__ == "__main__":
    client = Client()

    settings = fix.SessionSettings("Client.cfg")
    store_factory = fix.FileStoreFactory(settings)
    log_factory = fix.ScreenLogFactory(settings)
    initiator = fix.SocketInitiator(client, store_factory, settings, log_factory)
    initiator.start()
    print("FIX client started.")

    start_terminal_input(client)
