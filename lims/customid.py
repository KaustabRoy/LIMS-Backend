from .models import User
role_map = {
    1:"AD",
    2:"FD",
    5:"DR",
}

def customID(role:int) -> str:
    # print("Testing filter: none = ",(User.objects.filter(uid__istartswith=role_map[role]).last()== None))
    if (User.objects.filter(uid__istartswith=role_map[role]).last()== None):
        new_id = role_map[role]+"000"
        return new_id
    last_uid = User.objects.filter(uid__istartswith=role_map[role]).last().uid
    if last_uid is not None:    
        init = last_uid[:2]
        sl = last_uid[2:]
        n_sl = int(sl)
        n_sl += 1
        str_sl = str(n_sl)
        z_sl = str_sl.zfill(3)
        new_id = init+z_sl
        return new_id
    else:
        new_id = role_map[role]+"000"
        return new_id

def generate_org_uid(previous_uid = None) -> str:
    if previous_uid is not None:
        initial = previous_uid[:2]
        serial_number = int(previous_uid[2:])
        serial_number = serial_number + 1
        uid = initial + (str(serial_number).zfill(3))
    elif previous_uid is None:
        uid = "SH000"
    return uid
    
def on_role_change_generate_uid():
    pass

def generate_laboratory_id(previous_lab_id = None) -> str:
    if previous_lab_id is not None:
        initial = previous_lab_id[:1]
        serial_number = int(previous_lab_id[1:])
        serial_number = serial_number + 1
        # ---------- info start ----------
        print("inital = ", initial)
        print("new serial_number = ", serial_number)
        print("length of initial = ", len(previous_lab_id[:1]))
        print("length left after initial = ", len(previous_lab_id[1:]))
        print("length of serial number = ", len(str(serial_number)))
        print("number of zeroes = ", len(previous_lab_id[1:]) - len(str(serial_number)))
        # ---------- info end ----------
        lab_id = initial + (str(serial_number)).zfill(len(previous_lab_id[1:]))
    elif previous_lab_id is None:
        lab_id = "L000"
    return lab_id