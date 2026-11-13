# drafter-deployment-template-v1
Custom calendar management for TTRPGs

---
# Important notes:

> This project is intended to be broken into multiple files. When I tried to deploy it, I was getting a ModuleNotFound error for the other python files that were imported by `main`, so I just combined the files in main to get something that was running for Friday.

> The back-end logic that makes this program useful is not complete, but the front-end placeholders satisfy the majority of the functionality requirements, with some potential exceptions:
> - __The implementation of the State dataclass must have at least 4 fields__: I only have two, but one of them is a very complex dataclass with more than four attributes, so I hope that covers it. I couldn't think of additional things to add to the state that would still be meaningful.
> - __At least one field must be a list of class instances or a dictionary of class instances__: Same as above. I couldn't think of a meaningful way to use a list or dictionary of classes, but I'm hoping the complexity of the Year class—with its nested dataclass and lists of dataclasses as attributes—covers that.  
> - __The site should have a legitimate purpose or functionality__: This won't really be applicable until the back-end is done.
> - __Any advanced coding techniques (i.e. that weren't covered in this course) used are thoroughly documented in the code__: I documented anything I though was complex, but I don't recall what we have or have not done in this course, so there may be something I used without realizing it hadn't been explicitly taught in this course yet
