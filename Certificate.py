class Certificate:
    def __init__(self, block, view, signatures):
        self.block = block
        self.view = view
        self.signatures = signatures