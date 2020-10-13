from PyQt5.QtGui import QPainter, QColor, QPen, QPicture
from PyQt5.QtCore import Qt
from Model import Model
import MatrixShop 
import numpy as np
from ZBufferMethod import ZBuffer

class Renderer:
    @staticmethod
    def _render_all(models, project_matrix, model_matrix, context):
        transformation_matrix = transform_matrix_init(project_matrix, model_matrix, context)

        # преобразовать вершины умножив на матрицу
        transform_vertices = []
        for model in models:
            transform_vertices.append([*map(lambda vert: vert @ transformation_matrix, model.vertices)])

        #z-buffer work
        x_size, y_size = context.width(), context.height()
        transformed_models = []
        for transf_verts, model in zip(transform_vertices, models):
            new_model = Model().init_like(transf_verts, model.faces, model.color)
            transformed_models.append(new_model)

        z_buff = ZBuffer(transformed_models)
        z_buf, color_mask = z_buff.go(back_color=Qt.lightGray, x_size=x_size, y_size=y_size)
        return z_buf, color_mask

    @staticmethod
    def render_all_color(models, project_matrix, model_matrix, context):
        _, color_mask = Renderer._render_all(models, project_matrix, model_matrix, context)
        Renderer.render_from_color_mask(color_mask, context)
    
    @staticmethod
    def render_all_z_mask(models, project_matrix, model_matrix, context):
        z_buf, _ = Renderer._render_all(models, project_matrix, model_matrix, context)
        Renderer.render_from_z_mask(z_buf, context)
    
    @staticmethod
    def render_one(model: Model, project_matrix, model_matrix, context):

        transformation_matrix = transform_matrix_init(project_matrix, model_matrix, context)
        
        # преобразовать вершины умножив на матрицу
        transform_vertices = [*map(lambda vert: vert @ transformation_matrix, model.vertices)]

        #z-buffer work
        x_size, y_size = context.width(), context.height()
        z_buff = ZBuffer([Model().init_like(transform_vertices, model.faces, model.color)])
        z_buff_mask, color_mask = z_buff.go(back_color=Qt.lightGray, x_size=x_size, y_size=y_size)
        
        # рисовать
        Renderer.render_from_color_mask(color_mask, context)

    @staticmethod
    def prerender_all(models, project_matrix, model_matrix, context):

        transformation_matrix = transform_matrix_init(project_matrix, model_matrix, context)
        
        # преобразовать вершины умножив на матрицу
        transform_vertices = []
        for model in models:
            transform_vertices.append([*map(lambda vert: vert @ transformation_matrix, model.vertices)])

        #z-buffer work
        x_size, y_size = context.width(), context.height()
        transformed_models = []
        for transf_verts, model in zip(transform_vertices, models):
            new_model = Model().init_like(transf_verts, model.faces, model.color)
            transformed_models.append(new_model)

        z_buff = ZBuffer(transformed_models)
        generator = z_buff.step_by_step(back_color=Qt.lightGray, x_size=x_size, y_size=y_size)
        return generator

    @staticmethod
    def render_from_z_mask(z_buf_mask, context):
        z_buf_mask = convert_deep_to_alpha(z_buf_mask)
        # рисовать
        qp = QPainter()
        picture = QPicture()

        qp.begin(picture)
        for x in range(len(z_buf_mask)):
            for y in range(len(z_buf_mask[0])):

                # a = color_mask[x][y]
                a = QColor(Qt.black)
                a.setAlpha(z_buf_mask[x][y])

                qp.setPen(a)
                qp.drawPoint(x, y)
        qp.end()                     # painting done
        picture.save("drawing.pic")       # save picture

        picture = QPicture()
        picture.load("drawing.pic")           # load picture
        qp = QPainter()
        qp.begin(context)                # paint in myImage
        qp.drawPicture(0, 0, picture)    # draw the picture at (0,0)
        qp.end() 

    @staticmethod
    def render_from_color_mask(color_mask, context):
        qp = QPainter()
        picture = QPicture()

        qp.begin(picture)
        for x in range(len(color_mask)):
            for y in range(len(color_mask[0])):

                a = color_mask[x][y]
                qp.setPen(a)
                qp.drawPoint(x, y)
        qp.end()                     # painting done
        picture.save("drawing.pic")       # save picture

        picture = QPicture()
        picture.load("drawing.pic")           # load picture
        qp = QPainter()
        qp.begin(context)                # paint in myImage
        qp.drawPicture(0, 0, picture)    # draw the picture at (0,0)
        qp.end() 
        
def prepeare_to_screen(context) :
    scale = min(context.width(), context.height()) / 1.5
    scale_matrix = MatrixShop.dilation(scale, scale, scale)
    invert_matrix = MatrixShop.reflectionY()
    center_matrix = MatrixShop.translation(context.width() / 2, context.height() / 2, 0)

    return scale_matrix @ invert_matrix @ center_matrix

def convert_deep_to_alpha(z_buf):
    tmp = map((lambda line: list(filter(lambda n: not np.isinf(n), line))), z_buf)
    tmp = list(filter(lambda line: line != [], tmp))
    z_min = min(map(min, tmp))
    z_max = max(map(max, tmp))
    z_zero = z_min - 1
    
    z_buf = (map(lambda n: n if n != -np.inf else z_zero, line) for line in z_buf)
    to_procent = lambda x: int((x - z_zero) * 255 / (z_max - z_zero))
    z_buf = (map(to_procent, line) for line in z_buf)
    z_buf = list(map(list, z_buf))

    return z_buf

def transform_matrix_init(project_matrix, model_matrix, context):
    project_matrix[2,2] = 1
    transformation_matrix = model_matrix @ project_matrix # module viue projection matrix
    prep_to_scr = prepeare_to_screen(context)
    transformation_matrix = transformation_matrix @ prep_to_scr
    return transformation_matrix