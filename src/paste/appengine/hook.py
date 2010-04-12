import datetime


datastore_logs = []


def hook_datastore (service, call, request, response):
    log = {}
    log["time"] = datetime.datetime.now().strftime("%H:%M:%S.%f")
    qry = ""
    log["operation"] = call
    if call == "Put":
        for entity in request.entity_list():
            log["entity"] = entity.key().path().element_list()[0].type()
            for prop in entity.property_list():
                qry += prop.name() + ", "
            qry = qry[:-2]

    elif call == "RunQuery":
        log["entity"] = request.kind()
        qry = " where "
        for filter in request.filter_list():
            qry += filter.property_list()[0].name() + "=?,"
        qry = qry[:-1]
        qry += " limit " + str(request.offset()) + ", " + str(request.limit()) + ""

    elif call == "Get":
        qry = "GET"

    log["query"] = qry
    datastore_logs.append(log)
