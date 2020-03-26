import unittest

import node
import tree
import operator

def assert_equal(got, expected, msg):
    """
    Simple asset helper
    """
    assert expected == got, \
        "[{}] Expected: {}, got: {}".format(msg, expected, got)


class SimpleFunctionsTestCase(unittest.TestCase):

    def setUp(self):
        self.max_agg = lambda x, y: x if x > y else y
        self.tree = tree.Tree(self.max_agg)
        self.tree.create_root(5)

        self.xor_tree = tree.Tree(operator.xor)
        self.xor_tree.create_root(1)


    def test_can_insert_single(self):
        """
        Inserts a single node into the tree.

        r
        |
        A

        #score(1)
        """

        new_node = self.tree.new_node(10)
        self.tree.put(self.tree.root, new_node)

        # Check
        assert_equal(len(self.tree.root.children), 1, "root children")
        assert_equal(self.tree.root.subtree_value, 10, "root subtree value") 

    def test_can_insert_two(self):
        """
        Makes a simple tree.
        r
        | \
        A  B

        #score(1)
        """
        node_a = self.tree.new_node(10)
        node_b = self.tree.new_node(8)

        self.tree.put(self.tree.root, node_a)

        # Check
        assert_equal(len(self.tree.root.children), 1, "root children")
        assert_equal(self.tree.root.subtree_value, 10, "root subtree value")

        self.tree.put(self.tree.root, node_b)

        # check
        assert_equal(len(self.tree.root.children), 2, "root children")
        assert_equal(self.tree.root.subtree_value, 10, "root subtree value")

    def test_xor_tree(self):
        """
        Makes a simple tree.
        r
        | \
        A  B

        #score(1)        
        """
        node_a = self.xor_tree.new_node(0)
        node_b = self.xor_tree.new_node(1)

        self.xor_tree.put(self.xor_tree.root, node_a)

        # Check
        assert_equal(len(self.xor_tree.root.children), 1, "root children")
        assert_equal(self.xor_tree.root.subtree_value, 1, "root subtree value")

        self.xor_tree.put(self.xor_tree.root, node_b)

        # check
        assert_equal(len(self.xor_tree.root.children), 2, "root children")
        assert_equal(self.xor_tree.root.subtree_value, 0, "root subtree value")

    def test_bubble_up_value(self):
        """
        Addition of third level, should bubble up the values

        root
        |  \
        A  B
        |
        C
        |
        D

        #score(2)        
        """
        root = self.tree.root
        node_a = self.tree.new_node(4)
        node_b = self.tree.new_node(5)
        node_c = self.tree.new_node(6)
        node_d = self.tree.new_node(8)

        self.tree.put(root, node_a)
        self.tree.put(root, node_b)

        assert_equal(len(self.tree.root.children), 2, "root children")
        assert_equal(self.tree.root.subtree_value, 5, "root subtree value")

        self.tree.put(node_a, node_c)

        assert_equal(self.tree.root.subtree_value, 6, "root subtree value")
        assert_equal(node_a.subtree_value, 6, "node a subtrtee value")

        self.tree.put(node_a, node_c)
        self.tree.put(node_c, node_d)

        assert_equal(self.tree.root.subtree_value, 8, "root subtree value")
        assert_equal(node_a.subtree_value, 8, "node a subtree value")

    def test_simple_flatten_merge(self):
        """
        Flatten should merge

          r         r
        / |    >  /  |
        A  B     A  B_NEW
         / |
        C  D

        #score(2)
        """

        root = self.tree.root
        node_a = self.tree.new_node(4)
        node_b = self.tree.new_node(5)
        node_c = self.tree.new_node(5)
        node_d = self.tree.new_node(59)

        self.tree.put(root, node_a)
        self.tree.put(root, node_b)
        self.tree.put(node_b, node_c)
        self.tree.put(node_b, node_d)

        self.tree.flatten(node_b, operator.add)

        # It should be a leaf.
        assert_equal(len(node_b.children), 0, "node b children")
        assert node_b.is_external(), "Node should be leaf after flattening."

        # The node key should be the sum of the children.
        assert_equal(node_b.key, 69, "node b key")

    def test_example_swap(self):
        """
        Can perform swap as shown in example

           A(5)
           / \
         C(2) D(8)
          |
         B(10)

         > tree.swap(B, D)

           A(5)
           / \
         C(2) B(10)
          |
         D(8)

        #score(2)      
        """

        root = self.tree.root
        C = self.tree.new_node(2)
        B = self.tree.new_node(10)
        D = self.tree.new_node(8)

        self.tree.put(root, C)
        self.tree.put(root, D)
        self.tree.put(C, B)

        assert_equal(C.subtree_value, 10, "node c subtree value")
        assert_equal(root.subtree_value, 10, "root subtree value")

        self.tree.swap(B, D)

        assert_equal(C.subtree_value, 8, "node c subtree value")
        assert_equal(root.subtree_value, 10, "root subtree value")

    def test_simple_swap(self):
        """
        Swap subtree A and B correctly.

                root
              /  |   \
             A   B    C
           /  |      / \
          D   E     G   H
             /
            F

        swap(A, C)

                root
              /  |   \
             C   B    A
           /  |      / \
          G   H     D   E
                       /
                      F

        swap(F, C)

                root
              /  |   \
             F   B    A
                     / \
                    D   E
                       /
                      C
                    /  \
                   G    H

        #score(4)
        """

        # Generate the nodes
        root = self.tree.root
        node_a = self.tree.new_node(4)
        node_b = self.tree.new_node(5)
        node_c = self.tree.new_node(6)
        node_d = self.tree.new_node(7)
        node_e = self.tree.new_node(8)
        node_f = self.tree.new_node(9)
        node_g = self.tree.new_node(10)
        node_h = self.tree.new_node(11)

        # Put them into the tree.
        self.tree.put(root, node_a)
        self.tree.put(root, node_b)
        self.tree.put(root, node_c)
        self.tree.put(node_a, node_d)
        self.tree.put(node_a, node_e)
        self.tree.put(node_e, node_f)
        self.tree.put(node_c, node_g)
        self.tree.put(node_c, node_h)

        # Check that the values are correct
        assert_equal(root.subtree_value, 11, "root subtree value")
        assert_equal(node_c.subtree_value, 11, "node c subtree value")
        assert_equal(node_a.subtree_value, 9, "node a subtree value")

        # Let's get swapping!
        # ezmode
        self.tree.swap(node_a, node_c)

        assert_equal(root.subtree_value, 11, "root subtree value")
        assert_equal(node_c.subtree_value, 11, "node cd subtree value")
        assert_equal(node_a.subtree_value, 9, "node a subtree value")

        assert node_c.parent == root, "node c should be root's child"
        assert node_a.parent == root, "node a should be root's child"

        assert_equal(len(node_c.children), 2, "node c children")
        assert_equal(len(node_a.children), 2, "node a children")

        # ¯\_(ツ)_/¯
        self.tree.swap(node_f, node_c)

        # Root value should stay
        assert_equal(self.tree.root.subtree_value, 11, "root subtree value")

        # Parent and children should have swapped
        # correctly
        assert node_f.parent == root, "Node should swap parent."
        assert node_c.parent == node_e, "Node should swap parent."
        assert node_c in node_e.children, "Node should add children."

        # Values should be propagated.
        # subtree_values should look like:
        #         11
        #      /  |   \
        #     9  5    11
        #             / \
        #            7   11
        #               /
        #              11
        #            /  \
        #           10   11

        assert_equal(node_f.subtree_value, 9, "node f subtree value")

        assert_equal(node_a.subtree_value, 11, "node a subtree value")
        assert_equal(node_e.subtree_value, 11, "node e subtree value")
        assert_equal(node_c.subtree_value, 11, "node c subtree value")
        assert_equal(node_d.subtree_value, 7, "node d subtree value")


if __name__ == '__main__':
    unittest.main()
