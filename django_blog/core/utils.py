def parse_int(value:str, default=None):
    try:
        return int(value)
    except(ValueError, TypeError):
        return default
    
def to_lower_strip(value:str, default=None):
    try:
        return str(value.lower().strip())
    except(ValueError, TypeError):
        return default
    

def nest_comments(comments):
    root_comments = []
    comments_dict = {comment.id: comment for comment in comments}

    for comment in comments:
        parent_id = comment.reply_to
        if parent_id is None:
            root_comments.append(comment)
        else:
            parent = comments_dict.get(parent_id)
            if parent:
                if not hasattr(parent, 'replies'):
                    parent.replies = []
                parent.replies.append(comment)
    return root_comments
