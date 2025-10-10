class Node:
    """Класс для представления узла (вершины) графа"""

    def __init__(self, name, data=None):
        """
        Инициализация узла

        Args:
            name: имя/идентификатор узла
            data: дополнительные данные узла
        """
        self.name = name
        self.data = data
        self.neighbors = {}  # словарь соседей: {сосед: вес_ребра}

    def add_neighbor(self, neighbor, weight=1):
        """
        Добавление соседа к узлу

        Args:
            neighbor: соседний узел
            weight: вес ребра (по умолчанию 1)
        """
        self.neighbors[neighbor] = weight

    def remove_neighbor(self, neighbor):
        """
        Удаление соседа

        Args:
            neighbor: соседний узел для удаления
        """
        if neighbor in self.neighbors:
            del self.neighbors[neighbor]
        else: raise KeyError

    def get_neighbors(self):
        """Получение списка соседей"""
        return list(self.neighbors.keys())

    def get_weight(self, neighbor):
        """
        Получение веса ребра к соседу

        Args:
            neighbor: соседний узел
        """
        return self.neighbors.get(neighbor, None)

    def __str__(self):
        """Строковое представление узла"""
        return f"Node({self.name})"

    def __repr__(self):
        """Представление узла для отладки"""
        return f"Node({self.name})"


class Graph:
    """Класс для представления графа"""

    def __init__(self, directed=False):
        """
        Инициализация графа

        Args:
            directed: ориентированный ли граф (по умолчанию неориентированный)
        """
        self.nodes = {}  # словарь узлов: {имя: узел}
        self.directed = directed

    def add_node(self, name, data=None):
        """
        Добавление узла в граф

        Args:
            name: имя узла
            data: дополнительные данные узла
        """
        if name not in self.nodes:
            self.nodes[name] = Node(name, data)
        return self.nodes[name]

    def remove_node(self, name):
        """
        Удаление узла из графа

        Args:
            name: имя узла для удаления
        """
        if name in self.nodes:
            # Удаляем узел из списка соседей всех других узлов
            node_to_remove = self.nodes[name]
            for node in self.nodes.values():
                if node_to_remove in node.neighbors:
                    node.remove_neighbor(node_to_remove)

            # Удаляем узел из графа
            del self.nodes[name]

    def add_edge(self, node1_name, node2_name, weight=1):
        """
        Добавление ребра между узлами

        Args:
            node1_name: имя первого узла
            node2_name: имя второго узла
            weight: вес ребра
        """
        # Создаем узлы, если они не существуют
        node1 = self.add_node(node1_name)
        node2 = self.add_node(node2_name)

        # Добавляем связь
        node1.add_neighbor(node2, weight)

        # Если граф неориентированный, добавляем обратную связь
        if not self.directed:
            node2.add_neighbor(node1, weight)

    def remove_edge(self, node1_name, node2_name):
        """
        Удаление ребра между узлами

        Args:
            node1_name: имя первого узла
            node2_name: имя второго узла
        """
        if node1_name in self.nodes and node2_name in self.nodes:
            node1 = self.nodes[node1_name]
            node2 = self.nodes[node2_name]

            node1.remove_neighbor(node2)
            if not self.directed:
                node2.remove_neighbor(node1)

    def get_node(self, name):
        """
        Получение узла по имени

        Args:
            name: имя узла
        """
        return self.nodes.get(name, None)

    def get_all_nodes(self):
        """Получение списка всех узлов"""
        return list(self.nodes.values())

    def bfs(self, start_name):
        """
        Обход графа в ширину (BFS)

        Args:
            start_name: имя начального узла
        """
        if start_name not in self.nodes:
            return []

        visited = set()
        queue = [self.nodes[start_name]]
        result = []

        while queue:
            current = queue.pop(0)
            if current not in visited:
                visited.add(current)
                result.append(current.name)

                for neighbor in current.get_neighbors():
                    if neighbor not in visited:
                        queue.append(neighbor)

        return result

    def dfs(self, start_name):
        """
        Обход графа в глубину (DFS)

        Args:
            start_name: имя начального узла
        """
        if start_name not in self.nodes:
            return []

        visited = set()
        result = []

        def dfs_recursive(node):
            visited.add(node)
            result.append(node.name)

            for neighbor in node.get_neighbors():
                if neighbor not in visited:
                    dfs_recursive(neighbor)

        dfs_recursive(self.nodes[start_name])
        return result

    def __str__(self):
        """Строковое представление графа"""
        result = []
        for node in self.nodes.values():
            neighbors = [f"{neighbor.name}({weight})" for neighbor, weight in node.neighbors.items()]
            result.append(f"{node.name}: {', '.join(neighbors)}")

        return "\n".join(result)


# Пример использования и построения графа
def main():
    # Создаем неориентированный граф
    graph = Graph(directed=False)

    # Добавляем узлы и ребра
    graph.add_edge("A", "B", 5)
    graph.add_edge("A", "C", 3)
    graph.add_edge("B", "D", 2)
    graph.add_edge("C", "D", 4)
    graph.add_edge("D", "E", 1)
    graph.add_edge("E", "F", 6)

    # Выводим граф
    print("Структура графа:")
    print(graph)
    print()

    # Обход в ширину
    print("Обход в ширину (BFS) начиная с A:")
    print(graph.bfs("A"))
    print()

    # Обход в глубину
    print("Обход в глубину (DFS) начиная с A:")
    print(graph.dfs("A"))
    print()

    # Создаем ориентированный граф
    directed_graph = Graph(directed=True)

    # Добавляем узлы и ребра для ориентированного графа
    directed_graph.add_edge("X", "Y", 2)
    directed_graph.add_edge("Y", "Z", 3)
    directed_graph.add_edge("Z", "X", 1)  # Обратная связь

    print("Ориентированный граф:")
    print(directed_graph)
    print()

    # Демонстрация работы с узлами
    print("Информация об узле A:")
    node_a = graph.get_node("A")
    if node_a:
        print(f"Имя: {node_a.name}")
        print(f"Соседи: {[neighbor.name for neighbor in node_a.get_neighbors()]}")
        print(f"Вес до B: {node_a.get_weight(graph.get_node('B'))}")


if __name__ == "__main__":
    main()