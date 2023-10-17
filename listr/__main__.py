from .sqlistr import SQListr, Base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from os.path import isfile

engine = create_engine("sqlite:///listr.sqlite")
Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()

root = session.query(SQListr).filter(SQListr.parent_id == SQListr.id).first()
if root is None:
    print("Initializing Listr")
    root = SQListr("Woody's Listr")
    session.add(root)
    session.flush()
    root.parent_id = -1
    
    session.commit()

current_list = root

while True:
    # Print the current list and its children
    print(current_list)

    # Prompt the user for input
    user_input = input("Enter command (or 'quit' to exit): ").strip()

    if user_input.lower() == "quit":
        print("Exiting...")
        break
    elif user_input.isdigit():
        # Get child at the specified index
        index = int(user_input)-1
        if 0 <= index < len(current_list.children):
            current_list = current_list.children[index]
        else:
            print("Invalid index.")
    elif user_input.startswith("!"):
        # Complete the task at the specified index
        index = int(user_input[1:])
        if 0 <= index < len(current_list.children):
            current_list.children[index].complete()
            session.commit()
        else:
            print("Invalid index.")
    elif user_input.startswith("-"):
        # Remove the child at the specified index
        index = int(user_input[1:])
        if 0 <= index < len(current_list.children):
            current_list.remove_child(index)
            session.commit()
            print("Child removed.")
        else:
            print("Invalid index.")
    elif user_input == "<":
        # Go to the parent list
        if current_list.parent is not current_list:
            current_list = current_list.parent
        else:
            print("Already at the root.")
    else:
        new_item = SQListr(task=user_input)
        session.add(new_item)
        session.flush()  # Flush the session to assign an ID to the new item
        new_item.parent = current_list
        current_list.children.append(new_item)
        session.commit()
