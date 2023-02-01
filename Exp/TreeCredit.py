class CreditCalculator:
    # Every time calculate a new tree, should initilaize a new instance

    def __init__(self, max_depth=5, total_credit=100):
        self.max_depth = max_depth
        self.total_credit = total_credit
        self.depth_subtreesize_index = [0] * (max_depth + 1)  # the i-th element refers to the subtree size sum of all nodes at depth i
        self.D = 0  # Max depth of the current tree, start from 0
        self.credit_sum = 0     # Used to verify, the sum should equal to self.total_credit


    def __GetSubtreeSize(self, node, d):
        if (d >  self.max_depth):
            print('Tree depth exceeds MAX_DEPTH!')
            exit()

        subtree_size = 1
        node['depth'] = d

        if d > self.D:
            self.D = d
        for child in node['children']:
            subtree_size += self.__GetSubtreeSize(child, d+1)
        node['subtree_size'] = subtree_size

        self.depth_subtreesize_index[d] += subtree_size
        return subtree_size


    def __CalculateCredit(self, node):
        d = node['depth']
        if d == 0:
            node['credit'] = 0
        else:
            current_depth_credit = (2 ** (self.D - d) / (2 ** self.D - 1)) * self.total_credit
            credit = (node['subtree_size'] / self.depth_subtreesize_index[d]) * current_depth_credit
            node['credit'] = round(credit, 3)
        for child in node['children']:
            self.__CalculateCredit(child)

    
    def __CleanMetaInfo(self, node):
        if 'depth' in node:
            del node['depth']
        if 'subtree_size' in node:
            del node['subtree_size']
        for child in node['children']:
            self.__CleanMetaInfo(child)


    def verify (self, node):
        if 'credit' in node:
            self.credit_sum += node['credit']
        for child in node['children']:
            self.verify(child)


    def algorithm1(self, tree):
        self.__GetSubtreeSize(tree, 0)
        self.__CalculateCredit(tree)
        self.__CleanMetaInfo(tree)


    def minifyTreeSpace(self, node):
        # Replace key with shorter name
        if 'name' in node:
            node['n'] = node.pop('name')
        if 'dict' in node:
            node['d'] = node.pop('dict')
            node_dict = node['d']
            if 'type' in node_dict:
                node_dict['t'] = node_dict.pop('type')
                match node_dict['t']:
                    case 'undefined':
                        node_dict['t'] = 1
                    case 'null':
                        node_dict['t'] = 2
                    case 'array':
                        node_dict['t'] = 3
                    case 'string':
                        node_dict['t'] = 4
                    case 'object':
                        node_dict['t'] = 5
                    case 'function':
                        node_dict['t'] = 6
                    case 'number':
                        node_dict['t'] = 7
            if 'value' in node_dict:
                node_dict['v'] = node_dict.pop('value')
        if 'children' in node:
            node['c'] = node.pop('children')
        if 'credit' in node:
            node['x'] = node.pop('credit')
        
        for child in node['c']:
            self.minifyTreeSpace(child)