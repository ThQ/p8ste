import datetime


datastore_logs = []


def stringify_datastore_prop_value(prop):
    """
    Almost copy/paste from appengine/google/appengine/datastore/entity_pb.py
    """

    res = ""
    if prop.has_int64value_:
        res = prop.DebugFormatInt64(prop.int64value_)
    if prop.has_booleanvalue_:
        res = prop.DebugFormatBool(prop.booleanvalue_)
    if prop.has_stringvalue_:
        res = prop.DebugFormatString(prop.stringvalue_)
    if prop.has_doublevalue_:
        res = prop.DebugFormat(prop.doublevalue_)
    if prop.has_pointvalue_:
        res = prop.pointvalue_.__str__()
    if prop.has_uservalue_:
        res = prop.uservalue_.__str__()
    if prop.has_referencevalue_:
        res = prop.referencevalue_.__str__()
    return res


def arrayze_datastore_properties(prop_list):
    props = []
    for prop in prop_list:
        field = {}
        field["name"] = prop.name()
        field["value"] = stringify_datastore_prop_value(prop.value())
        props.append(field)

    return props


def arrayze_datastore_filters(filter_list):
    filters = []
    for filter in filter_list:
        prop = filter[0]
        field = {}
        field["name"] = prop.name()
        field["value"] = stringify_datastore_prop_value(prop.value())
        filters.append(field)

    return filters


def hook_datastore(service, call, request, response):
    log = {}
    log["time"] = datetime.datetime.now().strftime("%H:%M:%S.%f")
    qry = ""
    log["operation"] = call

    if call == "Put":
        for entity in request.entity_list():
            prop_list = entity.property_list()
            log["entity"] = entity.key().path().element_list()[0].type()
            log["fields"] = arrayze_datastore_properties(prop_list)

    elif call == "RunQuery":
        log["entity"] = request.kind()
        log["fields"] = []
        for filter in request.filter_list():
            prop_list = filter.property_list()
            log["fields"].extend(arrayze_datastore_properties(prop_list))
        qry = " limit "
        qry += str(request.offset())
        qry += ", "
        qry += str(request.limit())

    elif call == "Get":
        qry = "GET"

    log["query"] = qry
    datastore_logs.append(log)
