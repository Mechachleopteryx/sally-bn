# ----------------------------------------------------------------------------
#
# Sally BN: An Open-Source Framework for Bayesian Networks.
#
# ----------------------------------------------------------------------------
# GNU General Public License v2
#
#   This program is free software; you can redistribute it and/or modify
#   it under the terms of the GNU General Public License as published by
#   the Free Software Foundation; either version 2 of the License, or
#   (at your option) any later version.
#
#   This program is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#   GNU General Public License for more details.
#
#   You should have received a copy of the GNU General Public License along
#   with this program; if not, write to the Free Software Foundation, Inc.,
#   51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.
#
# ----------------------------------------------------------------------------

import math


vertex_radio = 30.0
box_width = 160
delta_state = 30
title_height = delta_state + 5

# Colors
color_green = [204.0 / 255, 229.0 / 255, 204.0 / 255]
color_dark_green = [5.0 / 255, 138.0 / 255, 0.0 / 255]
color_light_green = [230.0 / 255, 242.0 / 255, 230.0 / 255]
color_gray = 152.0 / 255, 152.0 / 255, 152.0 / 255
color_light_gray = 235 / 255.0, 235 / 255.0, 235 / 255.0
color_white = [255.0 / 255, 255.0 / 255, 255.0 / 255]


class GraphDrawer:
    def __init__(self, area):
        #### Objects to show #####
        self.dynamic_arrow = None
        # circles
        self.vertices = {}
        # highlighted circles
        self.selected_vertices = []
        # edges
        self.edges_type_vertex = []
        self.edges_type_box = []
        # boxes
        self.boxes = []
        self.selected_edges = []


        # Transform for scale
        self.transform = None
        # Translations
        self.translation = [0, 0]
        self.last_translation = [0, 0]
        # Scale and zoom
        self.scale = 1
        self.delta_zoom = 0.1

        ##Viewer mode
        self.viewer_mode = True

        self.area = area
        self.area.connect("motion-notify-event", self.on_motion_event)
        self.area.connect("draw", self.on_drawing_area_draw)
        self.area.connect("scroll-event", self.on_scroll)


        self.area.connect("button-press-event", self.on_button_press)
        self.area.connect("button-release-event", self.on_button_release)

        #Mouse events
        self.button_pressed = False
        self.clicked_point = None


    def transform_point(self, p):
        """ Transform a point based on applied scale.
        """
        new_p = self.transform.transform_point(p[0], p[1])
        return new_p

    def on_button_press(self, widget, event):
        """
        Button pressed on drawing area.
        """
        self.button_pressed = True
        p = [event.x, event.y]
        ## Click on edit area to TRANSLATE
        if event.button == 1:
            self.clicked_point = p
            # # For translation in drawing area.
            self.last_translation[0] += self.translation[0]
            self.last_translation[1] += self.translation[1]

    def on_button_release(self, widget, event):
        """
        Button release on the drawing area.
        """
        self.button_pressed = False

        # Right click or middle click does not matter
        if event.button > 1:
            return

        p = [event.x, event.y]

        dx, dy = [self.clicked_point[0] - p[0], self.clicked_point[1] - p[1]]
        click_distance = math.hypot(dx, dy)
        # normal click
        if click_distance < 10.0:
            self.translation = [0, 0]

        self.clicked_point = None

    def on_motion_event(self, widget, event):
        """
        Event generated by the mouse motion on the drawing area.
        """
        p = self.transform_point([event.x, event.y])

        if self.clicked_point is None:
            return

        #TODO translate node
        #if self.clicked_point is not None and self.mode == Mode.edit and self.selected_vetex is not None:
        #    self.vertex_locations[self.selected_vetex] = p
        #    self.area.queue_draw()

        # translate world  is not None  and
        if self.viewer_mode:
            p = [event.x, event.y]

            dx, dy = [self.clicked_point[0] - p[0], self.clicked_point[1] - p[1]]

            self.translation[0] = -dx / self.scale
            self.translation[1] = -dy / self.scale

            self.area.queue_draw()


    def on_scroll(self, widget, event):
        """
        Scroll event by the mouse. It modifies the scale for drawing.
        """
        self.scale -= self.delta_zoom * event.delta_y
        self.area.queue_draw()

    def on_drawing_area_draw(self, drawing_area, cairo):
        """
        Draw on the drawing area!
        """
        # Sacale
        cairo.scale(self.scale, self.scale)
        # Translate
        tx = self.translation[0] + self.last_translation[0]
        ty = self.translation[1] + self.last_translation[1]
        cairo.translate(tx, ty)
        # Get transformation
        self.transform = cairo.get_matrix()
        self.transform.invert()

        #### Drawing ####
        # Background
        self.draw_background(cairo)

        ## selected vertices
        for v in self.selected_vertices:
            self.draw_selected_vertex(cairo, v, self.vertices)

        ## dynamic arrow
        if self.dynamic_arrow is not None:
            tmp_v = {"I": self.vertices[self.selected_vetex], "F": self.tmp_arrow}
            tmp_e = [["I", "F"]]
            self.draw_directed_arrows(cairo, tmp_e, tmp_v, headarrow_d=0)

        for e in self.selected_edges:
            self.draw_selected_edge(cairo, e, self.vertices)

        # Draw edges
        self.draw_directed_arrows(cairo, self.edges_type_vertex, self.vertices)
        # Draw nodes
        self.draw_vertices(cairo, self.vertices)

        # Draw edges
        self.draw_arrow_box(cairo, self.edges_type_box, self.boxes)
        # Draw nodes
        #TODO boxes debe tener todo
        #self.draw_boxes(cairo, self.boxes, self.marginals, self.evidences)


    def restore_zoom(self):
        self.translation = [0, 0]
        self.last_translation = [0, 0]
        self.scale = 1
        self.area.queue_draw()

    def draw_background(self, cairo):
        cairo.set_source_rgb(1, 1, 1.0)
        cairo.rectangle(-10000, -10000, 100000, 1000000)
        cairo.fill()

    def draw_directed_arrows(self, cairo, edges, vertices, headarrow_d=vertex_radio):
        for edge in edges:
            x1, y1 = vertices[edge[0]]
            x2, y2 = vertices[edge[1]]
            dx, dy = float(x2 - x1), float(y2 - y1)

            # Avoid problem with atan
            if dx == 0:
                dx = 1

            cairo.set_source_rgb(0, 0, 0.0)
            cairo.move_to(x1, y1)
            cairo.line_to(x2, y2)
            cairo.stroke()

            #draw arrow
            d = math.hypot(dx, dy) - headarrow_d
            theta = math.atan(dy / dx)
            # adjust for atan
            s = 1.0
            if dx < 0:
                s = -1.0

            # arrow head (triangle)
            a = vertex_radio / 2.0
            b = vertex_radio / 3.5

            xt1 = x1 + s * d * math.cos(theta)
            yt1 = y1 + s * d * math.sin(theta)

            xt2 = x1 + s * (d - a) * math.cos(theta) - s * b * math.sin(theta)
            yt2 = y1 + s * (d - a) * math.sin(theta) + s * b * math.cos(theta)

            b = -b
            xt3 = x1 + s * (d - a) * math.cos(theta) - s * b * math.sin(theta)
            yt3 = y1 + s * (d - a) * math.sin(theta) + s * b * math.cos(theta)

            cairo.move_to(xt1, yt1)
            cairo.line_to(xt2, yt2)
            cairo.line_to(xt3, yt3)
            cairo.line_to(xt1, yt1)

            cairo.fill()

    def draw_selected_edge(self, cairo, selected_edge, vertex_locations):
        if selected_edge[1] in vertex_locations and selected_edge[0] in vertex_locations:
            x1, y1 = vertex_locations[selected_edge[0]]
            x2, y2 = vertex_locations[selected_edge[1]]

            cairo.set_source_rgb(244 / 255.0, 192 / 255.0, 125 / 255.0)
            cairo.set_line_width(9.1)
            cairo.move_to(x1, y1)
            cairo.line_to(x2, y2)
            cairo.stroke()
            cairo.set_line_width(2.0)
        else:
            print "Error drawing selected edge"

    def draw_selected_vertex(self, cairo, selected_vertex, vertex_locations):
        ## selected node
        if selected_vertex in vertex_locations:
            point = vertex_locations[selected_vertex]
            cairo.set_source_rgb(1, 0.8, 0.0)  # yellow
            cairo.arc(point[0], point[1], vertex_radio + 5, 0, 2 * 3.1416)
            cairo.fill()
        else:
            print "Error drawing selected vertex"

    def draw_vertices(self, cairo, vertex_locations):
        for vname, point in vertex_locations.items():
            ## Fill circle
            cairo.set_source_rgb(0.61, 0.75, 1.0)  # light blue
            cairo.arc(point[0], point[1], vertex_radio, 0, 2 * 3.1416)
            cairo.fill()

            ## Draw border
            cairo.set_source_rgb(0.22, 0.30, 0.66)  # blue
            cairo.arc(point[0], point[1], vertex_radio, 0, 2 * math.pi)
            cairo.stroke()

            ## Draw text
            text_position = vertex_radio + 15
            cairo.set_source_rgb(0.12, 0.20, 0.56)  # blue
            # cairo.select_font_face("Georgia", cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_BOLD)
            cairo.select_font_face("Georgia")

            cairo.set_font_size(14)

            xbearing, ybearing, width, height, xadvance, yadvance = (
                cairo.text_extents(vname))
            cairo.move_to(point[0] + 0.5 - xbearing - width / 2,
                          point[1] + text_position + 0.5 - ybearing - height / 2)
            cairo.show_text(vname)

    def draw_arrow_box(self, cairo, edges, vertex_locations):
        for edge in edges:
            x1, y1 = vertex_locations[edge[0]]
            x2, y2 = vertex_locations[edge[1]]
            dx, dy = float(x2 - x1), float(y2 - y1)

            # Avoid problem with atan
            if dx == 0:
                dx = 1

            cairo.set_source_rgb(0, 0, 0.0)
            cairo.move_to(x1, y1)
            cairo.line_to(x2, y2)
            cairo.stroke()

            #draw arrow
            # FIXME put the headarrow in the right place
            d = math.hypot(dx, dy) / 2
            theta = math.atan(dy / dx)
            # adjust for atan
            s = 1.0
            if dx < 0:
                s = -1.0

            # arrow head (triangle)
            a = vertex_radio / 2.0
            b = vertex_radio / 3.5

            xt1 = x1 + s * d * math.cos(theta)
            yt1 = y1 + s * d * math.sin(theta)
            xt2 = x1 + s * (d - a) * math.cos(theta) - s * b * math.sin(theta)
            yt2 = y1 + s * (d - a) * math.sin(theta) + s * b * math.cos(theta)

            b = -b
            xt3 = x1 + s * (d - a) * math.cos(theta) - s * b * math.sin(theta)
            yt3 = y1 + s * (d - a) * math.sin(theta) + s * b * math.cos(theta)

            cairo.move_to(xt1, yt1)
            cairo.line_to(xt2, yt2)
            cairo.line_to(xt3, yt3)
            cairo.line_to(xt1, yt1)
            cairo.fill()

    def point_in_state(self, p, vertex_locations, marginals):
        """
        :p point to evaluate [x,y]
        :param vertex_locations dic with name and point, ex. {"v1":[x,y]}
        :param marginals dic with marginal probabilities to all variables
            ex. {"v1":{"state1": 0.5, "state2": 0.5}}
        :return: ("vertex", "state")
        """
        x, y = p

        for v, v_position in vertex_locations.iteritems():
            # states of vertex
            v_states = marginals[v].keys()
            box_heigh = self._get_box_height(v_states)

            # go to left-upper corner
            x_corner = v_position[0] - box_width / 2.0
            y_corner = v_position[1] - box_heigh / 2.0

            #if point.x is not in range
            if not x_corner < x <= x_corner + box_width:
                continue

            # evaluate each state for p.y
            for i in range(len(v_states)):
                ny = y_corner + title_height + i * delta_state
                ny_next = y_corner + title_height + (i + 1) * delta_state

                if ny < y <= ny_next:
                    return v, v_states[i]
        return None

    def draw_boxes(self, cairo, vertex_locations, marginals, evidence):
        """
        Draw boxes for each variable with its marginal probabilities.
        :param cairo to draw
        :param vertex_locations dic with name and point, ex. {"v1":[x,y]}
        :param marginals dic with marginal probabilities to all variables
            ex. {"v1":{"state1": 0.5, "state2": 0.5}}
        :param evidence is a dictionary with vertex name and state {"vertex_name":"state"}
        """
        for vname, point in vertex_locations.items():
            v_states = marginals[vname].keys()
            is_evidence = vname in evidence
            # Rectangles
            px, py = point
            box_heigh = self._get_box_height(v_states)
            x_corner = px - box_width / 2.0
            y_corner = py - box_heigh / 2.0

            #Background for evidence
            if is_evidence:
                cairo.set_source_rgb(*color_gray)
                cairo.rectangle(x_corner - 3, y_corner - 3, box_width + 6, box_heigh + 6)
                cairo.fill()

            # Background
            cairo.set_source_rgb(*color_light_green)  # light green

            ## if is evidence
            if is_evidence:
                cairo.set_source_rgb(*color_light_gray)  # light gray

            cairo.rectangle(x_corner, y_corner, box_width, box_heigh)
            cairo.fill()

            # Title background
            cairo.set_source_rgb(*color_green)  # green
            cairo.rectangle(x_corner, y_corner, box_width, title_height)
            cairo.fill()

            ## Title text
            cairo.select_font_face("Georgia")
            cairo.set_source_rgb(*color_dark_green)  # dark green
            cairo.move_to(x_corner + 5, y_corner + 25)
            cairo.set_font_size(17)
            cairo.show_text(vname)

            # Background rectangle for prob value box
            rwidth = (box_width / 2 - 10)
            rheight = delta_state / 2.0 + 5.0

            # For each state
            for i in range(len(v_states)):
                ny = y_corner + title_height + (i + 1) * delta_state

                # Text for states
                cairo.select_font_face("Georgia")
                cairo.set_source_rgb(15.0 / 255, 158.0 / 255, 0.0 / 255)
                cairo.set_font_size(14)
                cairo.move_to(x_corner + 5, ny - 10)
                cairo.show_text(v_states[i][:11])

                ### Values
                rx = x_corner + box_width / 2.0
                ry = ny - 25.0

                # Prob rectangle
                cairo.set_source_rgb(*color_gray)  # gray
                cairo.rectangle(rx, ry, rwidth, rheight)
                cairo.fill()

                val = marginals[vname][v_states[i]]
                # Prob rectangle
                val_width = rwidth * val
                cairo.set_source_rgb(*color_dark_green)  # dark green
                cairo.rectangle(rx, ry, val_width, rheight)
                cairo.fill()

                # Text for value
                cairo.select_font_face("Georgia")
                cairo.set_source_rgb(*color_white)
                cairo.set_font_size(14)
                cairo.move_to(rx + 5, ny - 10)
                cairo.show_text(str(val * 100)[:5] + "")

                ## State line
                cairo.set_line_width(0.5)
                cairo.set_source_rgb(*color_green)  # green
                cairo.move_to(x_corner, ny)
                cairo.line_to(x_corner + box_width, ny)
                cairo.stroke()

            #Border
            cairo.set_line_width(0.5)
            cairo.set_source_rgb(*color_dark_green)
            cairo.rectangle(x_corner, y_corner, box_width, box_heigh)
            cairo.stroke()

            # Line title
            cairo.move_to(x_corner, y_corner + title_height)
            cairo.line_to(x_corner + box_width, y_corner + title_height)
            cairo.stroke()


    @staticmethod
    def _get_box_height(num_states):
        return title_height + delta_state * len(num_states)

    ######## SET GRAPHICAL OBJECTS
    def set_dynamic_arrow(self, dynamic_arrow):
        """ set a dynamic arrow to show based on mouse motion.
        """
        self.dynamic_arrow = dynamic_arrow
        self.area.queue_draw()

    def set_viewer_mode(self, active):
        self.viewer_mode = active

    def set_selected_vertices(self, selected_vertices):
        self.selected_vertices = selected_vertices

    def set_selected_edges(self, selected_edges):
        self.selected_edges = selected_edges

    def set_vertices(self, vertices):
        self.vertices = vertices

    def set_edges_type_vertex(self, edges):
        self.edges_type_vertex = edges

    def set_edges_type_box(self, edges):
        self.edges_type_box = edges

    def set_boxes(self, boxes):
        self.boxes = boxes

    def repaint(self):
        self.area.queue_draw()