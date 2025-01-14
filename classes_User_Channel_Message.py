class User:
    def __init__(self,id:int, name:str):
        self.id = id
        self.name = name

    def __repr__(self) -> str :
        return f'User(id={self.id}, name={self.name})'

    def to_dict(self):
        dict = {'id' : self.id, 'name' : self.name}
        return dict


class Channel:
    def __init__(self,id:int, name:str, member_ids : list):
        self.id = id
        self.name = name
        self.member_ids = member_ids
    def __repr__(self) -> str :
        return f'Channel(id={self.id}, name={self.name}, member_ids={self.member_ids})'
    
    def to_dict(self):
        dict = {'id' : self.id, 'name' : self.name, 'member_ids': self.member_ids}
        return dict


class Message:
    def __init__(self, id: int, reception_date: str, sender_id: int, channel: int, content: str):
        self.id = id
        self.reception_date = reception_date
        self.sender_id = sender_id
        self.channel = channel
        self.content = content

    def __repr__(self) -> str :
        return f'Message(id={self.id}, sender_id={self.sender_id}, channel={self.channel}, content={self.content})'

    def to_dict(self):
        dict = {'id' : self.id, 'reception_date' : self.reception_date, 'sender_id': self.sender_id, 'channel': self.channel, 'content': self.content}
        return dict
