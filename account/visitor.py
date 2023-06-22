class Visitor:
    def __init__(self, request):
        self.request = request
        self.session = self.request.session
        self.visitor = self.session.get('visitor', {})
        self.liked_key = 'liked_property'

    def create_liked_list(self):
        return self.visitor.get(self.liked_key, [])
    

    def check_liked_status(self, property_obj_pk):
        liked_list = self.create_liked_list()
        if property_obj_pk in liked_list:
            liked = True
        else:
            liked = False
        return liked

    def add_or_remove_liked_property(self, property_obj_pk): 
        liked_list = self.create_liked_list()
        if property_obj_pk not in liked_list:
            liked_list.append(property_obj_pk)
            liked = True
        else:
            liked_list.remove(property_obj_pk)
            liked = False
        self.visitor[self.liked_key] = liked_list
        self.save()
        return liked

    def save(self):
        self.session['visitor'] = self.visitor
        self.session.modified = True
