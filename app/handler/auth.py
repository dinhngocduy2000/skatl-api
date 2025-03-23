from controller.auth import AuthController


class AuthHandler:
    controller:AuthController
    def __init__(self,controller:AuthController):
        self.controller=controller

    async def login(self)->str:
        return "Login success"