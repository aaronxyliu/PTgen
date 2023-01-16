function analyzeVariable(v) {
    v_info = {}
    if (v == undefined) {
        v_info = {'type':'undefined', 'children':[]}
    }
    else if (v == null) {
        v_info = {'type':'null', 'children':[]}
    }
    else if (Array.isArray(v))
    {
        v_info = {'type':'array', 'value':v.length, 'children':[]}
    }
    else if (typeof(v) == 'string')
    {
        v_info = {'type':'string', 'value':v, 'children':[]}
    }
    else if (typeof(v) == 'object')
    {
        v_info = {'type':'object', 'children':Object.keys(v)}
    }
    else if (typeof(v) == 'function')
    {
        v_info = {'type':'function', 'children':Object.keys(v)}
    }
    else
    {
        //console.log(typeof(v))
        v_info = {'type':typeof(v), 'value':v, 'children':[]}
    }
    //console.log(v_info)
    return v_info
}