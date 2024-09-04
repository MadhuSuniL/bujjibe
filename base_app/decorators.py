 
def consumer_method_exception_handler(func):
    async def wrapper(self, *args, **kwargs):
        try:
            await func(self, *args, **kwargs)
        except Exception as e:
            await self.send_json({'detail': repr(e)})
            await self.close()
    return wrapper

