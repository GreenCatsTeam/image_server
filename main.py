from flask import Flask, make_response, send_file, request
import os
import uuid
import re
# import fcntl


# def acquire(lock_file):
#     open_mode = os.O_RDWR | os.O_CREAT | os.O_TRUNC
#     fd = os.open(lock_file, open_mode)

#     pid = os.getpid()
#     lock_file_fd = None
    
#     timeout = 5.0
#     start_time = current_time = time.time()
#     while current_time < start_time + timeout:
#         try:
#             # The LOCK_EX means that only one process can hold the lock
#             # The LOCK_NB means that the fcntl.flock() is not blocking
#             # and we are able to implement termination of while loop,
#             # when timeout is reached.
#             # More information here:
#             # https://docs.python.org/3/library/fcntl.html#fcntl.flock
#             fcntl.flock(fd, fcntl.LOCK_EX | fcntl.LOCK_NB)
#         except (IOError, OSError):
#             pass
#         else:
#             lock_file_fd = fd
#             break
#         print(f'  {pid} waiting for lock')
#         time.sleep(1.0)
#         current_time = time.time()
#     if lock_file_fd is None:
#         os.close(fd)
#     return lock_file_fd


# def release(lock_file_fd):
#     # Do not remove the lockfile:
#     #
#     #   https://github.com/benediktschmitt/py-filelock/issues/31
#     #   https://stackoverflow.com/questions/17708885/flock-removing-locked-file-without-race-condition
#     fcntl.flock(lock_file_fd, fcntl.LOCK_UN)
#     os.close(lock_file_fd)
#     return None


app = Flask(__name__)

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

compiled_re = re.compile("^[A-Za-z0-9-]*$")

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def correct_id(id):
    return len(id) == 36 and re.match(compiled_re, id)

@app.route("/get_img/<id>")
def get_file(id=None):
    if (id is None):
        return make_response("No id", 400)
    if (not correct_id(id)):
        return make_response("Wrong id format", 400)
    filename = os.path.join("pictures", str(id))
    print(filename)
    if (not os.path.exists(filename)):
        return make_response("File does not exists", 404)
    if (not os.path.isfile(filename)):
        return make_response("That is not a file", 400)
    # fd = acquire(filename)
    # if (fd is None):
    #     return make_response("Error when acquiring file mutex", 500)
    
    # f_buffer = os.fdopen(fd, "rb")

    # if (f_buffer is None):
    #     return make_response("Error when opening file", 500)
    
    
    return send_file(filename, as_attachment=True)

@app.route("/upload_img", methods=["POST"])
def upload_file():
    if 'file' not in request.files:
        # flash('No file part')
        return make_response("No file", 400)
    file = request.files['file']
    if file.filename == '':
        return make_response("No selected file", 400)
    if file and allowed_file(file.filename):
        # filename = secure_filename(file.filename)
        filename = str(uuid.uuid4())
        file.save(os.path.join("pictures", filename))
        return make_response(str(filename), 200)
    else:
        make_response("Nope", 400)
    
    

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5050, debug=False)