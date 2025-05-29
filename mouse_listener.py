from pynput import mouse

def start_rmb_listener(state):
    def on_click(x, y, button, pressed):
        from pynput.mouse import Button
        if button == Button.right:
            state["_rmb_down"] = pressed
    listener = mouse.Listener(on_click=on_click)
    listener.daemon = True
    listener.start()
    return listener