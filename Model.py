import pywavefront
import configparser
import numpy as np

class Model:

    def __init__(self):
        self.vertices = None
        self.faces = None
        self.color = None
    
    def init_like(self, vertices, faces, color):
        self.vertices = vertices
        self.faces = faces
        self.color = color

        return self
    
    def init_with_file(self, objName = None):
        objName = 'obj' if objName is None else objName

        config = configparser.ConfigParser()  # создаём объекта парсера
        config.read("settings.ini")  # читаем конфиг
        scene = pywavefront.Wavefront(config['path'][objName], collect_faces=True)
        
        self.vertices = np.array( [(*line, 1) for line in scene.vertices] ) # чтение вершин, плюс добавление w=1 к координатам вершин
        self.faces = scene.mesh_list[0].faces

        return self


    def get_edges(self, vertices = None):
        vertices = self.vertices if vertices is None else vertices

        all_edges = []
        for face in self.faces:
            paire_of_indexs = zip(face, (*face[1 : ], face[0])) #строка - это пара индексов вершин, эти вершины - начало и конец ребра
            for i_v1, i_v2 in paire_of_indexs:
                all_edges.append((vertices[i_v1], vertices[i_v2]))

        return all_edges

    def getAllFacesVerts(self, vertices = None):
        vertices = self.vertices if vertices is None else vertices

        return [[vertices[i_vert] for i_vert in face] for face in self.faces]

    @staticmethod
    def convert_from_homogenus_to_decard(vertices):
        decard_vertices = []
        for vert in vertices:
            w = vert[-1]
            dec_v = np.array([v / w for v in vert[: 2]])    # нужны только координаты x,y
            decard_vertices.append(dec_v)

        return decard_vertices
        

# a = Model()
# a.convert_fromhomogenus_to_decard(a.vertices)