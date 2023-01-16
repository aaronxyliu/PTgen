function createObjectTree(depth_limit = 5, debug = false) {

    class TreeNode {
        constructor(_name, _dict) {
            this.name = _name
            this.dict = _dict
            this.children = []
        }
    }

    function analyzeVariable(v) {
        let v_info = {}
        if (v == undefined) {
            v_info = { dict: { 'type': 'undefined' }, 'children': [] }
        }
        else if (v == null) {
            v_info = { dict: { 'type': 'null' }, 'children': [] }
        }
        // else if (v == window) {
        //     v_info = { dict: { 'type': 'window' }, 'children': [] }
        // }
        else if (Array.isArray(v)) {
            v_info = { dict: { 'type': 'array', 'value': v.length }, 'children': [] }
        }
        else if (typeof (v) == 'string') {
            v_info = { dict: { 'type': 'string', 'value': v }, 'children': [] }
        }
        else if (typeof (v) == 'object') {
            v_info = { dict: { 'type': 'object' }, 'children': Object.keys(v) }
        }
        else if (typeof (v) == 'function') {
            v_info = { dict: { 'type': 'function' }, 'children': Object.keys(v) }
        }
        else {
            v_info = { dict: { 'type': typeof (v), 'value': v }, 'children': [] }
        }
        return v_info
    }

    function hasSameAddr(prefix, v) {
        // Prevent loop in the object tree
        // Check whether v points to some parent variable
        parent_v = prefix
        _v = `${prefix}["${v}"]`
        if (eval(`typeof (${_v}) != 'object' && typeof (${_v}) != 'function'`)) 
            return false
        while (true) {
            // Has Same Address
            if (eval(`typeof (${parent_v}) == 'object' || typeof (${parent_v}) == 'function'`))
                if (eval(`${parent_v} == ${_v}`))
                    return true
            index = parent_v.lastIndexOf('[')
            if (index == -1)
                break
            parent_v = parent_v.slice(0, index)
        }
        return false
    }
    
    var node_cnt = 0;
    var max_depth = 0;
    function generateTree(parent, prefix, v_name, depth = 1) {
        if (depth > depth_limit) {
            return
        }
        if (hasSameAddr(prefix, v_name)) {
            return
        }
        v_info = {}
        if (debug)
            console.log(`${prefix}["${v_name}"]   depth: ${depth}`)
        eval(`v_info = analyzeVariable(${prefix}["${v_name}"]);`)
        let node = new TreeNode(v_name, v_info.dict)
        node_cnt += 1
        parent.children.push(node)
    
        for (let child_v_name of v_info['children']) {
            generateTree(node, `${prefix}["${v_name}"]`,child_v_name, depth + 1)
        }
    }


    var tree = new TreeNode('window', { 'type': 'string' })
    var vlist = Object.keys(window)


    this.fetch(`../static/origin.json`)
        .then((response) => response.json())
        .then((origin_vlist) => {
            vlist = vlist.filter(val => !origin_vlist.includes(val));

            node_cnt = 0;
            max_depth = 0;
            for (v of vlist) {
                generateTree(tree, 'window', v)
            }
            if (debug) {
                console.log(`Node number: ${node_cnt}`)
                console.log(`Max depth: ${max_depth}`)
                console.log(tree)
            }
            var display_div = document.getElementById('obj-tree');
            display_div.innerHTML = JSON.stringify(tree);
        })
}


