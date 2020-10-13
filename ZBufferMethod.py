import Model
import Intermediary
import numpy as np

class ZBuffer:
    def __init__(self, figures: list):
        self.figures = figures
    
    def _init_process(self, z_of_plane, x_size, y_size, color = None):
        self.z_mask = np.full((x_size, y_size), z_of_plane)
        self.z_color = [[color] * y_size for _ in range(x_size)]

    @staticmethod
    def _equation_of_plane(face):
        v1, v2, v3 = face
        vect1 = np.array(v2) - np.array(v1)
        vect2 = np.array(v3) - np.array(v1)

        vect = np.cross(vect1[:-1], vect2[:-1])

        D = -vect @ v1[:-1]

        return *vect, D
    
    @staticmethod
    def _edges_init(face):
        all_y = list(map(lambda vert: vert[1], face))

        y_top = max(all_y)
        y_low = min(all_y)
        
        if y_top == y_low:
            edges_pair_1 = [(face[0], face[1]), (face[1], face[2])]
            edges_pair_2 = [(face[1], face[2]), (face[2], face[0])]
            return (edges_pair_1, edges_pair_2)

        i_vert_top = all_y.index(y_top)
        i_vert_low = all_y.index(y_low)
        i_vert_middle = (set((0, 1, 2)) - set((i_vert_low, i_vert_top))).pop()

        v_top = face[i_vert_top]
        v_low = face[i_vert_low]
        v_middle = face[i_vert_middle]

        # две пары рёбер треугольника
        # первя пара, та, что нахоится выше по y, вторая та что ниже
        edges_pair_1 = [(v_top, v_middle), (v_top, v_low)]
        edges_pair_2 = [(v_middle, v_low), (v_top, v_low)]

        return (edges_pair_1, edges_pair_2)

    def _have_z(self, x, y, z, color):
        if x >= len(self.z_mask) or y >= len(self.z_mask[0]): return

        if self.z_mask[x][y] < z:
            self.z_mask[x][y] = z
            self.z_color[x][y] = color

    # z_of_plane -- координата z отсекающей плоскости. Т.е. если хочешь добавить "стену", стоящую на сцене, нужно подать z этой стены
    def step_by_step(self,*, z_of_plane = -np.inf, back_color, x_size, y_size):
        
        self._init_process(z_of_plane, x_size, y_size, back_color)

        for figure in self.figures:
     
            for face in figure.getAllFacesVerts():
                
                A, B, C, D = self._equation_of_plane(face)
                edges_pairs = self._edges_init(face)

                for edg_left, edg_right in edges_pairs:
                    if C == 0: 
                        break

                    y_top = min(edg_left[0][1], edg_right[0][1])
                    y_low = max(edg_left[1][1], edg_right[1][1])

                    # если общая точка для двух рёбер сверху, то
                    if edg_left[0][0] == edg_right[0][0]:
                        x1, x2, x3 = edg_left[0][0], edg_left[1][0], edg_right[1][0]
                        y1, y2, y3 = edg_left[0][1], edg_left[1][1], edg_right[1][1]
                    else:
                        x1, x2, x3 = edg_left[1][0], edg_left[0][0], edg_right[0][0]
                        y1, y2, y3 = edg_left[1][1], edg_left[0][1], edg_right[0][1]

                    for y in np.arange(y_top, y_low - 1, -1):
                        if y_top == y_low:
                            # ситуация возможна в двух случаях, когда одна из граней треугольника(face) лежит перпендикулярно y
                            # или когда вся плоскость перпедикулярна y 
                            verts_on_line = []
                            for vert in (*edg_left, *edg_right):
                                if vert[1] == y_top: verts_on_line.append(vert[0])
                            
                            x_a, x_b = min(verts_on_line), max(verts_on_line)
                        else:
                            x_a = x1 + (x2 - x1) * (y - y1) / (y2 - y1)
                            x_b = x1 + (x3 - x1) * (y - y1) / (y3 - y1)

                            if x_b < x_a:
                                x_a, x_b = x_b, x_a

                        z = -(A * x_a + B * y + D) / C + A/C
                        for x in np.arange(x_a, x_b + 1):
                            z -= A / C
                            self._have_z(int(x), int(y), z, figure.color)
                        # with open('img.txt', 'w', encoding='utf8') as file:
                        #     for line in self.z_mask:
                        #         file.write(''.join(map(str, line)))
                        #         file.write('\n')
                yield self.z_mask, self.z_color
    
        #return self.z_mask, self.z_color
    def go(self,*, z_of_plane = -np.inf, back_color, x_size, y_size):
        
        for _ in self.step_by_step(z_of_plane=z_of_plane, back_color=back_color, x_size=x_size, y_size=y_size):
            ...
        return self.z_mask, self.z_color