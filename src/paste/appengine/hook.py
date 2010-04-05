import datetime


datastore_logs = []


def hook_datastore (service, call, request, response):
    qry = "<" + datetime.datetime.now().strftime("%H:%M:%S.%f") + "> "

    if call == "Put":
        qry += "PUT into "
        for entity in request.entity_list():
            qry += entity.key().path().element_list()[0].type()
            qry += " entity "
            for prop in entity.property_list():
                qry += prop.name() + ", "
            qry = qry[:-2]

    elif call == "RunQuery":
        qry += "FETCH from " + request.kind() + ""
        qry += " where "
        for filter in request.filter_list():
            qry += filter.property_list()[0].name() + "=?,"
        qry = qry[:-1]
        qry += " limit " + str(request.offset()) + ", " + str(request.limit()) + ""

    elif call == "Get":
        qry += "GET"

    datastore_logs.append(qry)
