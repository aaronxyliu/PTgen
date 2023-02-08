function createObjectTree(depth_limit = 5, node_limit = 500, debug = false) {

    class TreeNode {
        constructor(_name) {
            this.name = _name
            this.dict = {}
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
        else if (Array.isArray(v)) {
            v_info = { dict: { 'type': 'array', 'value': v.length }, 'children': [] }
        }
        else if (typeof (v) == 'string') {
            v_info = { dict: { 'type': 'string', 'value': v.slice(0, 10) }, 'children': [] }
        }
        else if (typeof (v) == 'object') {
            v_info = { dict: { 'type': 'object' }, 'children': Object.keys(v) }
        }
        else if (typeof (v) == 'function') {
            v_info = { dict: { 'type': 'function' }, 'children': Object.keys(v) }
        }
        else if (typeof (v) == 'number') {
            v_info = { dict: { 'type': 'number', 'value': v.toFixed(2)}, 'children': [] }
        }
        else {
            v_info = { dict: { 'type': typeof (v), 'value': v }, 'children': [] }
        }
        return v_info
    }

    // function hasSameAddr(prefix, v) {
    //     // Prevent loop in the object tree
    //     // Check whether v points to some parent variable
    //     if (!prefix)
    //         return false
    //     let _v = `${prefix}["${v}"]`

    //     if (eval(`typeof (${_v}) != 'object' && typeof (${_v}) != 'function'`)) 
    //         return false
    //     if (eval(`typeof (${prefix}) == 'object' || typeof (${prefix}) == 'function'`))
    //         if (eval(`${prefix} == ${_v}`))
    //             return true
        
    //     let needClose = true
    //     for(let p = prefix.length - 1; p > 0; p -= 1) {        
    //         if (needClose && prefix[p-1] == '"' && prefix[p] == ']') {
    //             needClose = false
    //             p-=1
    //         }
    //         else if (prefix[p-1] == '[' && prefix[p] == '"') {
    //             needClose = true
    //             let parent_v = prefix.slice(0, p-1)
    //                 if (eval(`typeof (${parent_v}) == 'object' || typeof (${parent_v}) == 'function'`))
    //                     if (eval(`${parent_v} == ${_v}`))
    //                         return true
    //         }
    //     }

    //     return false
    // }

    function hasCircle(v_path) {
        // Prevent loop in the object tree
        // Check whether v points to some parent variable
        if (v_path.length <= 1) 
            return false

        cur_v = 'window'
        for (let v of v_path) {
            cur_v += `["${v}"]`
        }

        if (eval(`typeof (${cur_v}) != 'object' && typeof (${cur_v}) != 'function'`)) 
            return false

        ancient_v = 'window'
        for (let i = 0; i < v_path.length - 1; i += 1) {
            ancient_v += `["${v_path[i]}"]`
            if (eval(`typeof (${ancient_v}) == 'object' || typeof (${ancient_v}) == 'function'`))
                if (eval(`${ancient_v} == ${cur_v}`))
                    return true
        }

        return false
    }
    
    // var node_cnt = 0;
    // function generateTree(parent, prefix, v_name, depth = 1) {
    //     if (depth > depth_limit) {
    //         return
    //     }
    //     if (node_cnt >= node_limit) {
    //         return
    //     }

    //     if (v_name == "\\") {
    //         v_name += '\\'  // add slash for special name
    //     }
    //     if (hasSameAddr(prefix, v_name)) {
    //         return
    //     }
        
    //     let v_info = {}
    //     if (debug)
    //         console.log(`${prefix}["${v_name}"]   depth: ${depth}`)
    //     eval(`v_info = analyzeVariable(${prefix}["${v_name}"]);`)
    //     let node = new TreeNode(v_name, v_info.dict)
    //     node_cnt += 1
    //     parent.children.push(node)
    
    //     for (let child_v_name of v_info['children']) {
    //         generateTree(node, `${prefix}["${v_name}"]`,child_v_name, depth + 1)
    //     }
    // }

    function genPTree(node_limit, depth_limit, blacklist) {
        // BFS
        let circle_num = 0
        let node_num = 1
        var root = new TreeNode('window')
        let q = []      // Property Path Queue
        let qc = []     // Generated Property Tree Queue
        q.push([])
        qc.push(root)

        while (q.length) {
            let v_path = q.shift()
            let cur_node = qc.shift()

            if (hasCircle(v_path)) {
                circle_num += 1
                continue
            }

            v_str = 'window'
            for (let v of v_path) {
                v_str += `["${v}"]`
            }
            
            if (debug)
                console.log(`${v_str}   depth: ${v_path.length}`)
            
            let v_info = {}
            eval(`v_info = analyzeVariable(${v_str});`)
            if (cur_node.name != v_path[v_path.length - 1]) {
                console.log('ERROR: UNMATACHED NODES.')
            }

            cur_node.dict = v_info.dict

            // Remove global variables in blacklist
            if (v_path.length == 0)
                v_info['children'] = v_info['children'].filter(val => !blacklist.includes(val));
            
            if (v_path.length < depth_limit) {
                for (let child of v_info['children']) {
                    if (node_num >= node_limit)
                        break
                        
                    let c_node = new TreeNode(child)    
                    cur_node.children.push(c_node)
                    q.push([...v_path])              // shallow copy
                    q[q.length - 1].push(child)
                    qc.push(c_node)
                    node_num += 1
                }
            }
            
        }
        return [root, node_num, circle_num]
    }


    // var tree = new TreeNode('window', { 'type': 'object' })
    // var vlist = Object.keys(window)


    this.fetch(`../static/origin.json`)
        .then((response) => response.json())
        .then((origin_vlist) => {

            let tree_info = genPTree(500, 5, origin_vlist)
            let tree = tree_info[0]

            if (debug) {
                console.log(`Node number: ${tree_info[1]}   Circle number: ${tree_info[2]}`)
                console.log(tree)
            }
            let circle_num_div = document.getElementById('circle-num');
            circle_num_div.innerHTML = tree_info[2];

            let json_str = JSON.stringify(tree);
            let display_div = document.getElementById('obj-tree');
            display_div.innerHTML = json_str.replace(/<|>/g, '_');
        })
}


function getGlobalV() {
    var vlist = Object.keys(window)


    this.fetch(`../static/origin.json`)
        .then((response) => response.json())
        .then((origin_vlist) => {
            vlist = vlist.filter(val => !origin_vlist.includes(val));
            let json_str = JSON.stringify(vlist);
            let display_div = document.getElementById('gloabl-v');

            // Replace '<' and '>' with '_' to prevent the conflict with web tag
            display_div.innerHTML = json_str.replace(/<|>/g, '_')
        })
}


