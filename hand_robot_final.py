# ================================================================================
#   2023-12-19

#   .py 파일 실행 후 마우스와 키보드 입력으로 움직임 입력
#   각 부위를 마우스로 클릭하면 빨간색으로 활성화 됨
#   활성화 된 부위에 키보드 값을 입력해 회전 적용
#
#   < 키보드 매뉴얼 >
#   - 상측 버튼(↑): 손가락 굽히기, 손목 관절과 각 손가락 관절에 적용 가능
#   - 하측 버튼(↓): 손가락 펴기, 손목 관절과 각 손가락 관절에 적용 가능
#   - 좌측 버튼(←): 손가락 벌리기/모으기, 손목 관절과 각 손가락의 첫번째 관절만 적용 가능
#   - 우측 버튼(←): 손가락 벌리기/모으기, 손목 관절과 각 손가락의 첫번째 관절만 적용 가능
# ================================================================================

import vtk
from vtkmodules.vtkCommonColor import vtkNamedColors
from vtkmodules.vtkFiltersSources import (
    vtkSphereSource,
    vtkCubeSource,
    vtkCylinderSource
)
from vtkmodules.vtkInteractionStyle import vtkInteractorStyleTrackballCamera
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkPolyDataMapper,
    vtkPropPicker,
    vtkProperty,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer
)


colors = vtkNamedColors()
NUMBER_OF_SPHERES = 10

renderer = vtkRenderer()
renderer.SetBackground(colors.GetColor3d('White'))

renwin = vtkRenderWindow()
renwin.AddRenderer(renderer)
renwin.SetSize(640, 480)
renwin.SetWindowName('Final Project_Hand')

# An interactor
interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(renwin)

thumb_jnt1Actor = vtkActor()
thumb_jnt2Actor = vtkActor()
thumb_jnt3Actor = vtkActor()

index_jnt3Actor = vtkActor()
middle_jnt3Actor = vtkActor()
ring_jnt3Actor = vtkActor()
pinky_jnt3Actor = vtkActor()


class CustomInteractorStyle(vtkInteractorStyleTrackballCamera):

    def __init__(self, parent=None):
        self.parent = interactor
        self.AddObserver("LeftButtonPressEvent", self.leftButtonPressEvent)
        self.AddObserver("KeyPressEvent", self.keyPressEvent)

        self.LastPickedActor = None
        self.LastPickedProperty = vtkProperty()


    def leftButtonPressEvent(self, obj, event):
        clickPos = self.GetInteractor().GetEventPosition()

        picker = vtkPropPicker()
        picker.Pick(clickPos[0], clickPos[1], 0, self.GetDefaultRenderer())

        # get the new
        self.NewPickedActor = picker.GetActor()

        # If something was selected
        if self.NewPickedActor:
            # If we picked something before, reset its property
            if self.LastPickedActor:
                self.LastPickedActor.GetProperty().DeepCopy(self.LastPickedProperty)

            # Save the property of the picked actor so that we can
            # restore it next time
            self.LastPickedProperty.DeepCopy(self.NewPickedActor.GetProperty())
            # Highlight the picked actor by changing its properties
            self.NewPickedActor.GetProperty().SetColor(colors.GetColor3d('Red'))
            self.NewPickedActor.GetProperty().SetDiffuse(1.0)
            self.NewPickedActor.GetProperty().SetSpecular(0.0)
            self.NewPickedActor.GetProperty().EdgeVisibilityOn()

            # save the last picked actor
            self.LastPickedActor = self.NewPickedActor
            name = self.LastPickedActor.GetObjectName()
            print('{} was clicked'.format(name))

        self.OnLeftButtonDown()

        return

    def rotationTransform(self, actor, angle):
        transform = self.actor.GetUserTransform()
        pos = self.actor.GetPosition()

        transform.Translate(pos[0], pos[1], pos[2])
        transform.RotateX(angle)
        transform.Translate(-pos[0], -pos[1], -pos[2])




    def keyPressEvent(self, obj, event):
        key = self.parent.GetKeySym()
        transform = self.LastPickedActor.GetUserTransform()
        pos = self.LastPickedActor.GetPosition()
        name = self.LastPickedActor.GetObjectName()

        if key == 'Up':
            i = 0
            while i >= -2:
                transform.Translate(pos[0], pos[1], pos[2])
                if 'jnt' in name:
                    if 'thumb' in name:
                        transform.RotateZ(i * 0.3)
                        transform.RotateX(i)
                    else:
                        transform.RotateX(i)
                transform.Translate(-pos[0], -pos[1], -pos[2])
                renwin.Render()
                i -= 2
            print(key, 'was pressed')

        if key == 'Down':
            i = 0
            while i <= 2:
                transform.Translate(pos[0], pos[1], pos[2])
                if 'jnt' in name:
                    if 'thumb' in name:
                        transform.RotateX(i)
                        transform.RotateZ(i * 0.3)
                    else:
                        transform.RotateX(i)
                transform.Translate(-pos[0], -pos[1], -pos[2])
                renwin.Render()
                i += 2
            print(key, 'was pressed')

        if key == 'Left':
            i = 0
            while i <= 2:
                if 'jnt1' in name:
                    transform.Translate(pos[0], pos[1], pos[2])
                    transform.RotateZ(i)
                    transform.Translate(-pos[0], -pos[1], -pos[2])
                renwin.Render()
                i += 2
            print(key, 'was pressed')

        if key == 'Right':
            i = 0
            while i >= -2:
                if 'jnt1' in name:
                    transform.Translate(pos[0], pos[1], pos[2])
                    transform.RotateZ(i)
                    transform.Translate(-pos[0], -pos[1], -pos[2])
                renwin.Render()
                i -= 2
            print(key, 'was pressed')
        return




def main():

    # add the custom style
    style = CustomInteractorStyle()
    style.SetDefaultRenderer(renderer)
    interactor.SetInteractorStyle(style)

    #======================================== palm ========================================

    palm = vtkCubeSource()
    palm.SetXLength(12.5)
    palm.SetYLength(10)
    palm.SetZLength(1)

    palmMapper = vtkPolyDataMapper()
    palmMapper.SetInputConnection(palm.GetOutputPort())

    palmTransform = vtk.vtkTransform()
    palmActor = vtkActor()
    palmActor.SetUserTransform(palmTransform)
    palmActor.SetMapper(palmMapper)
    palmActor.GetProperty().SetColor(colors.GetColor3d("RoyalBLue"))

    palmPos = palmActor.GetPosition()

    # carpal1
    carpal1 = vtkCubeSource()
    carpal1.SetXLength(1)
    carpal1.SetYLength(12)
    carpal1.SetZLength(1)

    carpal1Mapper = vtkPolyDataMapper()
    carpal1Mapper.SetInputConnection(carpal1.GetOutputPort())

    carpal1Actor = vtkActor()
    carpal1Actor.SetOrigin(palmPos[0], palmPos[1] - palm.GetYLength() / 2, palmPos[2])
    carpal1Actor.RotateZ(25)
    carpal1Actor.SetUserTransform(palmTransform)
    carpal1Actor.SetMapper(carpal1Mapper)
    carpal1Actor.GetProperty().SetColor(colors.GetColor3d("RoyalBLue"))

    # carpal2
    carpal2 = vtkCubeSource()
    carpal2.SetXLength(1)
    carpal2.SetYLength(12)
    carpal2.SetZLength(1)

    carpal2Mapper = vtkPolyDataMapper()
    carpal2Mapper.SetInputConnection(carpal2.GetOutputPort())

    carpal2Actor = vtkActor()
    carpal2Actor.SetOrigin(palmPos[0], palmPos[1] - palm.GetYLength() / 2, palmPos[2])
    carpal2Actor.RotateZ(7.5)
    carpal2Actor.SetUserTransform(palmTransform)
    carpal2Actor.SetMapper(carpal2Mapper)
    carpal2Actor.GetProperty().SetColor(colors.GetColor3d("RoyalBLue"))

    carpal1Actor.SetPosition(palmPos[0], palmPos[1], palmPos[2])

    # carpal3
    carpal3 = vtkCubeSource()
    carpal3.SetXLength(1)
    carpal3.SetYLength(12)
    carpal3.SetZLength(1)

    carpal3Mapper = vtkPolyDataMapper()
    carpal3Mapper.SetInputConnection(carpal3.GetOutputPort())

    carpal3Actor = vtkActor()
    carpal3Actor.SetOrigin(palmPos[0], palmPos[1] - palm.GetYLength() / 2, palmPos[2])
    carpal3Actor.RotateZ(-7.5)
    carpal3Actor.SetUserTransform(palmTransform)
    carpal3Actor.SetMapper(carpal3Mapper)
    carpal3Actor.GetProperty().SetColor(colors.GetColor3d("RoyalBLue"))

    # carpal4
    carpal4 = vtkCubeSource()
    carpal4.SetXLength(1)
    carpal4.SetYLength(12)
    carpal4.SetZLength(1)

    carpal4Mapper = vtkPolyDataMapper()
    carpal4Mapper.SetInputConnection(carpal4.GetOutputPort())

    carpal4Actor = vtkActor()
    carpal4Actor.SetOrigin(palmPos[0], palmPos[1] - palm.GetYLength() / 2, palmPos[2])
    carpal4Actor.RotateZ(-25)
    carpal4Actor.SetUserTransform(palmTransform)
    carpal4Actor.SetMapper(carpal4Mapper)
    carpal4Actor.GetProperty().SetColor(colors.GetColor3d("RoyalBLue"))

    # carpal0
    carpal0 = vtkCubeSource()
    carpal0.SetXLength(1)
    carpal0.SetYLength(6)
    carpal0.SetZLength(1)

    carpal0Mapper = vtkPolyDataMapper()
    carpal0Mapper.SetInputConnection(carpal0.GetOutputPort())

    carpal0Actor = vtkActor()
    carpal0Actor.SetOrigin(palmPos[0] + 1.5, palmPos[1] - palm.GetYLength() / 2, palmPos[2])
    carpal0Actor.RotateZ(80)
    carpal0Actor.SetUserTransform(palmTransform)
    carpal0Actor.SetMapper(carpal0Mapper)
    carpal0Actor.GetProperty().SetColor(colors.GetColor3d("RoyalBLue"))

    # wrist jnt
    wrist_jnt = vtkSphereSource()
    wrist_jnt.SetRadius(1.75)
    wrist_jnt.SetPhiResolution(20)
    wrist_jnt.SetThetaResolution(20)

    wrist_jntMapper = vtkPolyDataMapper()
    wrist_jntMapper.SetInputConnection(wrist_jnt.GetOutputPort())

    wrist_jntActor = vtkActor()
    wrist_jntActor.SetUserTransform(palmTransform)
    wrist_jntActor.SetMapper(wrist_jntMapper)
    wrist_jntActor.SetObjectName('wrist_jnt')
    wrist_jntActor.GetProperty().SetColor(colors.GetColor3d('Grey'))

    wrist_jntActor.SetPosition(palmPos[0], palmPos[1] - palm.GetYLength() * 0.6, palmPos[2])


    #==================================== finger_jnt1 ====================================

    # index_jnt1
    index_jnt1 = vtkSphereSource()
    index_jnt1.SetRadius(1.5)
    index_jnt1.SetPhiResolution(20)
    index_jnt1.SetThetaResolution(20)

    index_jnt1Mapper = vtkPolyDataMapper()
    index_jnt1Mapper.SetInputConnection(index_jnt1.GetOutputPort())

    index_jnt1Transform = vtk.vtkTransform()
    index_jnt1Transform.SetInput(palmTransform)

    index_jnt1Actor = vtkActor()
    index_jnt1Actor.SetUserTransform(index_jnt1Transform)
    index_jnt1Actor.SetMapper(index_jnt1Mapper)
    index_jnt1Actor.SetObjectName('index_jnt1')
    index_jnt1Actor.GetProperty().SetColor(colors.GetColor3d('Grey'))

    index_jnt1Actor.SetPosition(palmPos[0] - palm.GetXLength()/2 + index_jnt1.GetRadius(),
                                palmPos[1] + palm.GetYLength()/2 + index_jnt1.GetRadius() * 0.75,
                                palmPos[2])

    # middle_jnt1
    middle_jnt1 = vtkSphereSource()
    middle_jnt1.SetRadius(1.5)
    middle_jnt1.SetPhiResolution(20)
    middle_jnt1.SetThetaResolution(20)

    middle_jnt1Mapper = vtkPolyDataMapper()
    middle_jnt1Mapper.SetInputConnection(middle_jnt1.GetOutputPort())

    middle_jnt1Transform = vtk.vtkTransform()
    middle_jnt1Transform.SetInput(palmTransform)

    middle_jnt1Actor = vtkActor()
    middle_jnt1Actor.SetUserTransform(middle_jnt1Transform)
    middle_jnt1Actor.SetMapper(middle_jnt1Mapper)
    middle_jnt1Actor.SetObjectName('middle_jnt1')
    middle_jnt1Actor.GetProperty().SetColor(colors.GetColor3d('Grey'))

    middle_jnt1Actor.SetPosition(palmPos[0] - palm.GetXLength() * 0.25 + index_jnt1.GetRadius(), palmPos[1] + palm.GetYLength() / 2 + middle_jnt1.GetRadius() * 0.75, palmPos[2])

    # ring_jnt1
    ring_jnt1 = vtkSphereSource()
    ring_jnt1.SetRadius(1.5)
    ring_jnt1.SetPhiResolution(20)
    ring_jnt1.SetThetaResolution(20)

    ring_jnt1Mapper = vtkPolyDataMapper()
    ring_jnt1Mapper.SetInputConnection(ring_jnt1.GetOutputPort())

    ring_jnt1Transform = vtk.vtkTransform()
    ring_jnt1Transform.SetInput(palmTransform)

    ring_jnt1Actor = vtkActor()
    ring_jnt1Actor.SetUserTransform(ring_jnt1Transform)
    ring_jnt1Actor.SetMapper(ring_jnt1Mapper)
    ring_jnt1Actor.SetObjectName('ring_jnt1')
    ring_jnt1Actor.GetProperty().SetColor(colors.GetColor3d('Grey'))

    ring_jnt1Actor.SetPosition(palmPos[0] + palm.GetXLength() * 0.25 - index_jnt1.GetRadius(),
                               palmPos[1] + palm.GetYLength() / 2 + ring_jnt1.GetRadius() * 0.75,
                               palmPos[2])

    # pinky_jnt1
    pinky_jnt1 = vtkSphereSource()
    pinky_jnt1.SetRadius(1.5)
    pinky_jnt1.SetPhiResolution(20)
    pinky_jnt1.SetThetaResolution(20)

    pinky_jnt1Mapper = vtkPolyDataMapper()
    pinky_jnt1Mapper.SetInputConnection(pinky_jnt1.GetOutputPort())

    pinky_jnt1Transform = vtk.vtkTransform()
    pinky_jnt1Transform.SetInput(palmTransform)

    pinky_jnt1Actor = vtkActor()
    pinky_jnt1Actor.SetUserTransform(pinky_jnt1Transform)
    pinky_jnt1Actor.SetMapper(pinky_jnt1Mapper)
    pinky_jnt1Actor.SetObjectName('pinky_jnt1')
    pinky_jnt1Actor.GetProperty().SetColor(colors.GetColor3d('Grey'))

    pinky_jnt1Actor.SetPosition(palmPos[0] + palm.GetXLength() / 2 - pinky_jnt1.GetRadius(),
                             palmPos[1] + palm.GetYLength() / 2 + pinky_jnt1.GetRadius() * 0.75,
                             palmPos[2])

    # thumb_jnt1
    thumb_jnt1 = vtkSphereSource()
    thumb_jnt1.SetRadius(1.5)
    thumb_jnt1.SetPhiResolution(20)
    thumb_jnt1.SetThetaResolution(20)

    thumb_jnt1Mapper = vtkPolyDataMapper()
    thumb_jnt1Mapper.SetInputConnection(thumb_jnt1.GetOutputPort())

    thumb_jnt1Transform = vtk.vtkTransform()
    thumb_jnt1Transform.SetInput(palmTransform)

    # thumb_jnt1Actor = vtkActor()
    thumb_jnt1Actor.SetUserTransform(thumb_jnt1Transform)
    thumb_jnt1Actor.SetMapper(thumb_jnt1Mapper)
    thumb_jnt1Actor.SetObjectName('thumb_jnt1')
    thumb_jnt1Actor.GetProperty().SetColor(colors.GetColor3d('Grey'))

    thumb_jnt1Actor.SetPosition(palmPos[0] - palm.GetXLength() / 2 + thumb_jnt1.GetRadius() * 0.5, palmPos[1] - palm.GetYLength() / 2, palmPos[2])

    thumb_jnt1Pos = thumb_jnt1Actor.GetPosition()
    thumb_jnt1Transform.Translate(thumb_jnt1Pos[0], thumb_jnt1Pos[1], thumb_jnt1Pos[2])
    thumb_jnt1Transform.RotateZ(35)
    thumb_jnt1Transform.Translate(-thumb_jnt1Pos[0], -thumb_jnt1Pos[1], -thumb_jnt1Pos[2])


    #====================================== finger1 ======================================

    # index1
    index1 = vtkCylinderSource()
    index1.SetRadius(1.5)
    index1.SetHeight(4.5)
    index1.SetResolution(20)

    index1Mapper = vtkPolyDataMapper()
    index1Mapper.SetInputConnection(index1.GetOutputPort())

    index1Actor = vtkActor()
    index1Actor.SetUserTransform(index_jnt1Transform)
    index1Actor.SetMapper(index1Mapper)
    index1Actor.GetProperty().SetColor(colors.GetColor3d("RoyalBLue"))

    index_jnt1Pos = index_jnt1Actor.GetPosition()
    index1Actor.SetPosition(index_jnt1Pos[0],
                         index_jnt1Pos[1] + index_jnt1.GetRadius() / 2 + index1.GetHeight() / 2,
                         index_jnt1Pos[2])

    # middle1
    middle1 = vtkCylinderSource()
    middle1.SetRadius(1.5)
    middle1.SetHeight(5)
    middle1.SetResolution(20)

    middle1Mapper = vtkPolyDataMapper()
    middle1Mapper.SetInputConnection(middle1.GetOutputPort())

    middle1Actor = vtkActor()
    middle1Actor.SetUserTransform(middle_jnt1Transform)
    middle1Actor.SetMapper(middle1Mapper)
    middle1Actor.GetProperty().SetColor(colors.GetColor3d("RoyalBLue"))

    middle_jnt1Pos = middle_jnt1Actor.GetPosition()
    middle1Actor.SetPosition(middle_jnt1Pos[0],
                             middle_jnt1Pos[1] + middle_jnt1.GetRadius() / 2 + middle1.GetHeight() / 2,
                             middle_jnt1Pos[2])

    # ring1
    ring1 = vtkCylinderSource()
    ring1.SetRadius(1.5)
    ring1.SetHeight(4.5)
    ring1.SetResolution(20)

    ring1Mapper = vtkPolyDataMapper()
    ring1Mapper.SetInputConnection(ring1.GetOutputPort())

    ring1Actor = vtkActor()
    ring1Actor.SetUserTransform(ring_jnt1Transform)
    ring1Actor.SetMapper(ring1Mapper)
    ring1Actor.GetProperty().SetColor(colors.GetColor3d("RoyalBLue"))

    ring_jnt1Pos = ring_jnt1Actor.GetPosition()
    ring1Actor.SetPosition(ring_jnt1Pos[0],
                           ring_jnt1Pos[1] + ring_jnt1.GetRadius() / 2 + ring1.GetHeight()/2,
                           ring_jnt1Pos[2])

    # pinky1
    pinky1 = vtkCylinderSource()
    pinky1.SetRadius(1.5)
    pinky1.SetHeight(3.5)
    pinky1.SetResolution(20)

    pinky1Mapper = vtkPolyDataMapper()
    pinky1Mapper.SetInputConnection(pinky1.GetOutputPort())

    pinky1Actor = vtkActor()
    pinky1Actor.SetUserTransform(pinky_jnt1Transform)
    pinky1Actor.SetMapper(pinky1Mapper)
    pinky1Actor.GetProperty().SetColor(colors.GetColor3d("RoyalBLue"))

    pinky_jnt1Pos = pinky_jnt1Actor.GetPosition()
    pinky1Actor.SetPosition(pinky_jnt1Pos[0],
                        pinky_jnt1Pos[1] + pinky_jnt1.GetRadius() / 2 + pinky1.GetHeight() / 2,
                        pinky_jnt1Pos[2])
    
    # thumb1
    thumb1 = vtkCylinderSource()
    thumb1.SetRadius(1.5)
    thumb1.SetHeight(3)
    thumb1.SetResolution(20)

    thumb1Mapper = vtkPolyDataMapper()
    thumb1Mapper.SetInputConnection(thumb1.GetOutputPort())

    thumb1Actor = vtkActor()
    thumb1Actor.SetUserTransform(thumb_jnt1Transform)
    thumb1Actor.SetMapper(thumb1Mapper)
    thumb1Actor.GetProperty().SetColor(colors.GetColor3d("RoyalBLue"))

    thumb1Actor.SetPosition(thumb_jnt1Pos[0],
                        thumb_jnt1Pos[1] + thumb_jnt1.GetRadius() / 2 + thumb1.GetHeight() / 2,
                        thumb_jnt1Pos[2])


    #==================================== finger_jnt2 ====================================

    # index_jnt2
    index_jnt2 = vtkSphereSource()
    index_jnt2.SetRadius(1.5)
    index_jnt2.SetPhiResolution(20)
    index_jnt2.SetThetaResolution(20)

    index_jnt2Mapper = vtkPolyDataMapper()
    index_jnt2Mapper.SetInputConnection(index_jnt2.GetOutputPort())

    index_jnt2Transform = vtk.vtkTransform()
    index_jnt2Transform.SetInput(index_jnt1Transform)

    index_jnt2Actor = vtkActor()
    index_jnt2Actor.SetUserTransform(index_jnt2Transform)
    index_jnt2Actor.SetMapper(index_jnt2Mapper)
    index_jnt2Actor.SetObjectName('index_jnt2')
    index_jnt2Actor.GetProperty().SetColor(colors.GetColor3d('Grey'))

    index1Pos = index1Actor.GetPosition()
    index_jnt2Actor.SetPosition(index1Pos[0],
                         index1Pos[1] + index1.GetHeight() / 2 + index_jnt2.GetRadius() * 0.75,
                         index1Pos[2])

    # middle_jnt2
    middle_jnt2 = vtkSphereSource()
    middle_jnt2.SetRadius(1.5)
    middle_jnt2.SetPhiResolution(20)
    middle_jnt2.SetThetaResolution(20)

    middle_jnt2Mapper = vtkPolyDataMapper()
    middle_jnt2Mapper.SetInputConnection(middle_jnt2.GetOutputPort())

    middle_jnt2Transform = vtk.vtkTransform()
    middle_jnt2Transform.SetInput(middle_jnt1Transform)

    middle_jnt2Actor = vtkActor()
    middle_jnt2Actor.SetUserTransform(middle_jnt2Transform)
    middle_jnt2Actor.SetMapper(middle_jnt2Mapper)
    middle_jnt2Actor.SetObjectName('middle_jnt2')
    middle_jnt2Actor.GetProperty().SetColor(colors.GetColor3d('Grey'))

    middle1Pos = middle1Actor.GetPosition()
    middle_jnt2Actor.SetPosition(middle1Pos[0],
                       middle1Pos[1] + middle1.GetHeight() / 2 + middle_jnt2.GetRadius() * 0.75,
                       middle1Pos[2])

    # ring_jnt2
    ring_jnt2 = vtkSphereSource()
    ring_jnt2.SetRadius(1.5)
    ring_jnt2.SetPhiResolution(20)
    ring_jnt2.SetThetaResolution(20)

    ring_jnt2Mapper = vtkPolyDataMapper()
    ring_jnt2Mapper.SetInputConnection(ring_jnt2.GetOutputPort())

    ring_jnt2Transform = vtk.vtkTransform()
    ring_jnt2Transform.SetInput(ring_jnt1Transform)

    ring_jnt2Actor = vtkActor()
    ring_jnt2Actor.SetUserTransform(ring_jnt2Transform)
    ring_jnt2Actor.SetMapper(ring_jnt2Mapper)
    ring_jnt2Actor.SetObjectName('ring_jnt2')
    ring_jnt2Actor.GetProperty().SetColor(colors.GetColor3d('Grey'))

    ring1Pos = ring1Actor.GetPosition()
    ring_jnt2Actor.SetPosition(ring1Pos[0],
                          ring1Pos[1] + ring1.GetHeight() / 2 + ring_jnt2.GetRadius() * 0.75,
                          ring1Pos[2])

    # pinky_jnt2
    pinky_jnt2 = vtkSphereSource()
    pinky_jnt2.SetRadius(1.5)
    pinky_jnt2.SetPhiResolution(20)
    pinky_jnt2.SetThetaResolution(20)

    pinky_jnt2Mapper = vtkPolyDataMapper()
    pinky_jnt2Mapper.SetInputConnection(pinky_jnt2.GetOutputPort())

    pinky_jnt2Transform = vtk.vtkTransform()
    pinky_jnt2Transform.SetInput(pinky_jnt1Transform)

    pinky_jnt2Actor = vtkActor()
    pinky_jnt2Actor.SetUserTransform(pinky_jnt2Transform)
    pinky_jnt2Actor.SetMapper(pinky_jnt2Mapper)
    pinky_jnt2Actor.SetObjectName('pinky_jnt2')
    pinky_jnt2Actor.GetProperty().SetColor(colors.GetColor3d('Grey'))

    pinky1Pos = pinky1Actor.GetPosition()
    pinky_jnt2Actor.SetPosition(pinky1Pos[0],
                          pinky1Pos[1] + pinky1.GetHeight() / 2 + pinky_jnt2.GetRadius() * 0.75,
                          pinky1Pos[2])

    # thumb_jnt2
    thumb_jnt2 = vtkSphereSource()
    thumb_jnt2.SetRadius(1.5)
    thumb_jnt2.SetPhiResolution(20)
    thumb_jnt2.SetThetaResolution(20)

    thumb_jnt2Mapper = vtkPolyDataMapper()
    thumb_jnt2Mapper.SetInputConnection(thumb_jnt2.GetOutputPort())

    thumb_jnt2Transform = vtk.vtkTransform()
    thumb_jnt2Transform.SetInput(thumb_jnt1Transform)

    # thumb_jnt2Actor = vtkActor()
    thumb_jnt2Actor.SetUserTransform(thumb_jnt2Transform)
    thumb_jnt2Actor.SetMapper(thumb_jnt2Mapper)
    thumb_jnt2Actor.SetObjectName('thumb_jnt2')
    thumb_jnt2Actor.GetProperty().SetColor(colors.GetColor3d('Grey'))

    thumb1Pos = thumb1Actor.GetPosition()
    thumb_jnt2Actor.SetPosition(thumb1Pos[0],
                           thumb1Pos[1] + thumb1.GetHeight() / 2 + thumb_jnt2.GetRadius() * 0.75,
                           thumb1Pos[2])

    thumb_jnt2Pos = thumb_jnt2Actor.GetPosition()
    thumb_jnt2Transform.Translate(thumb_jnt2Pos[0], thumb_jnt2Pos[1], thumb_jnt2Pos[2])
    thumb_jnt2Transform.RotateZ(-15)
    thumb_jnt2Transform.Translate(-thumb_jnt2Pos[0], -thumb_jnt2Pos[1], -thumb_jnt2Pos[2])


    # ====================================== finger2 ======================================

    # index2
    index2 = vtkCylinderSource()
    index2.SetRadius(1.5)
    index2.SetHeight(3.5)
    index2.SetResolution(20)

    index2Mapper = vtkPolyDataMapper()
    index2Mapper.SetInputConnection(index2.GetOutputPort())

    index2Actor = vtkActor()
    index2Actor.SetUserTransform(index_jnt2Transform)
    index2Actor.SetMapper(index2Mapper)
    index2Actor.GetProperty().SetColor(colors.GetColor3d("RoyalBLue"))

    index_jnt2Pos = index_jnt2Actor.GetPosition()
    index2Actor.SetPosition(index_jnt2Pos[0],
                         index_jnt2Pos[1] + index_jnt2.GetRadius() / 2 + index2.GetHeight() / 2,
                         index_jnt2Pos[2])

    # middle2
    middle2 = vtkCylinderSource()
    middle2.SetRadius(1.5)
    middle2.SetHeight(4)
    middle2.SetResolution(20)

    middle2Mapper = vtkPolyDataMapper()
    middle2Mapper.SetInputConnection(middle2.GetOutputPort())

    middle2Actor = vtkActor()
    middle2Actor.SetUserTransform(middle_jnt2Transform)
    middle2Actor.SetMapper(middle2Mapper)
    middle2Actor.GetProperty().SetColor(colors.GetColor3d("RoyalBLue"))

    middle_jnt2Pos = middle_jnt2Actor.GetPosition()
    middle2Actor.SetPosition(middle_jnt2Pos[0],
                      middle_jnt2Pos[1] + middle_jnt2.GetRadius() / 2 + middle2.GetHeight() / 2,
                      middle_jnt2Pos[2])

    # ring2
    ring2 = vtkCylinderSource()
    ring2.SetRadius(1.5)
    ring2.SetHeight(3.5)
    ring2.SetResolution(20)

    ring2Mapper = vtkPolyDataMapper()
    ring2Mapper.SetInputConnection(ring2.GetOutputPort())

    ring2Actor = vtkActor()
    ring2Actor.SetUserTransform(ring_jnt2Transform)
    ring2Actor.SetMapper(ring2Mapper)
    ring2Actor.GetProperty().SetColor(colors.GetColor3d("RoyalBLue"))

    ring_jnt2Pos = ring_jnt2Actor.GetPosition()
    ring2Actor.SetPosition(ring_jnt2Pos[0],
                           ring_jnt2Pos[1] + ring_jnt2.GetRadius() / 2 + ring2.GetHeight() / 2,
                           ring_jnt2Pos[2])

    # pinky2
    pinky2 = vtkCylinderSource()
    pinky2.SetRadius(1.5)
    pinky2.SetHeight(3)
    pinky2.SetResolution(20)

    pinky2Mapper = vtkPolyDataMapper()
    pinky2Mapper.SetInputConnection(pinky2.GetOutputPort())

    pinky2Actor = vtkActor()
    pinky2Actor.SetUserTransform(pinky_jnt2Transform)
    pinky2Actor.SetMapper(pinky2Mapper)
    pinky2Actor.GetProperty().SetColor(colors.GetColor3d("RoyalBLue"))

    pinky_jnt2Pos = pinky_jnt2Actor.GetPosition()
    pinky2Actor.SetPosition(pinky_jnt2Pos[0],
                         pinky_jnt2Pos[1] + pinky_jnt2.GetRadius() / 2 + pinky2.GetHeight() / 2,
                         pinky_jnt2Pos[2])
    
    # thumb2
    thumb2 = vtkCylinderSource()
    thumb2.SetRadius(1.5)
    thumb2.SetHeight(3)
    thumb2.SetResolution(20)

    thumb2Mapper = vtkPolyDataMapper()
    thumb2Mapper.SetInputConnection(thumb2.GetOutputPort())

    thumb2Actor = vtkActor()
    thumb2Actor.SetUserTransform(thumb_jnt2Transform)
    thumb2Actor.SetMapper(thumb2Mapper)
    thumb2Actor.GetProperty().SetColor(colors.GetColor3d("RoyalBLue"))

    thumb2Actor.SetPosition(thumb_jnt2Pos[0],
                       thumb_jnt2Pos[1] + thumb_jnt2.GetRadius() / 2 + thumb2.GetHeight() / 2,
                       thumb_jnt2Pos[2])


    # ==================================== finger_jnt3 ====================================

    # index_jnt3
    index_jnt3 = vtkSphereSource()
    index_jnt3.SetRadius(1.5)
    index_jnt3.SetPhiResolution(20)
    index_jnt3.SetThetaResolution(20)

    index_jnt3Mapper = vtkPolyDataMapper()
    index_jnt3Mapper.SetInputConnection(index_jnt3.GetOutputPort())

    index_jnt3Transform = vtk.vtkTransform()
    index_jnt3Transform.SetInput(index_jnt2Transform)

    # index_jnt3Actor = vtkActor()
    index_jnt3Actor.SetUserTransform(index_jnt3Transform)
    index_jnt3Actor.SetMapper(index_jnt3Mapper)
    index_jnt3Actor.SetObjectName('index_jnt3')
    index_jnt3Actor.GetProperty().SetColor(colors.GetColor3d('Grey'))

    index2Pos = index2Actor.GetPosition()
    index_jnt3Actor.SetPosition(index2Pos[0],
                          index2Pos[1] + index2.GetHeight() / 2 + index_jnt3.GetRadius() * 0.75,
                          index2Pos[2])


    # middle_jnt3
    middle_jnt3 = vtkSphereSource()
    middle_jnt3.SetRadius(1.5)
    middle_jnt3.SetPhiResolution(20)
    middle_jnt3.SetThetaResolution(20)

    middle_jnt3Mapper = vtkPolyDataMapper()
    middle_jnt3Mapper.SetInputConnection(middle_jnt3.GetOutputPort())

    middle_jnt3Transform = vtk.vtkTransform()
    middle_jnt3Transform.SetInput(middle_jnt2Transform)

    middle_jnt3Actor.SetUserTransform(middle_jnt3Transform)
    middle_jnt3Actor.SetMapper(middle_jnt3Mapper)
    middle_jnt3Actor.SetObjectName('middle_jnt3')
    middle_jnt3Actor.GetProperty().SetColor(colors.GetColor3d('Grey'))

    middle2Pos = middle2Actor.GetPosition()
    middle_jnt3Actor.SetPosition(middle2Pos[0],
                       middle2Pos[1] + middle2.GetHeight() / 2 + middle_jnt3.GetRadius() * 0.75,
                       middle2Pos[2])

    # ring_jnt3
    ring_jnt3 = vtkSphereSource()
    ring_jnt3.SetRadius(1.5)
    ring_jnt3.SetPhiResolution(20)
    ring_jnt3.SetThetaResolution(20)

    ring_jnt3Mapper = vtkPolyDataMapper()
    ring_jnt3Mapper.SetInputConnection(ring_jnt3.GetOutputPort())

    ring_jnt3Transform = vtk.vtkTransform()
    ring_jnt3Transform.SetInput(ring_jnt2Transform)

    ring_jnt3Actor.SetUserTransform(ring_jnt3Transform)
    ring_jnt3Actor.SetMapper(ring_jnt3Mapper)
    ring_jnt3Actor.SetObjectName('ring_jnt3')
    ring_jnt3Actor.GetProperty().SetColor(colors.GetColor3d('Grey'))

    ring2Pos = ring2Actor.GetPosition()
    ring_jnt3Actor.SetPosition(ring2Pos[0],
                           ring2Pos[1] + ring2.GetHeight() / 2 + ring_jnt3.GetRadius() * 0.75,
                           ring2Pos[2])

    # pinky_jnt3
    pinky_jnt3 = vtkSphereSource()
    pinky_jnt3.SetRadius(1.5)
    pinky_jnt3.SetPhiResolution(20)
    pinky_jnt3.SetThetaResolution(20)

    pinky_jnt3Mapper = vtkPolyDataMapper()
    pinky_jnt3Mapper.SetInputConnection(pinky_jnt3.GetOutputPort())

    pinky_jnt3Transform = vtk.vtkTransform()
    pinky_jnt3Transform.SetInput(pinky_jnt2Transform)

    pinky_jnt3Actor.SetUserTransform(pinky_jnt3Transform)
    pinky_jnt3Actor.SetMapper(pinky_jnt3Mapper)
    pinky_jnt3Actor.SetObjectName('pinky_jnt3')
    pinky_jnt3Actor.GetProperty().SetColor(colors.GetColor3d('Grey'))

    pinky2Pos = pinky2Actor.GetPosition()
    pinky_jnt3Actor.SetPosition(pinky2Pos[0],
                          pinky2Pos[1] + pinky2.GetHeight() / 2 + pinky_jnt3.GetRadius() * 0.75,
                          pinky2Pos[2])
    
    # thumb_jnt3
    thumb_jnt3 = vtkSphereSource()
    thumb_jnt3.SetRadius(1.5)
    thumb_jnt3.SetPhiResolution(20)
    thumb_jnt3.SetThetaResolution(20)

    thumb_jnt3Mapper = vtkPolyDataMapper()
    thumb_jnt3Mapper.SetInputConnection(thumb_jnt3.GetOutputPort())

    thumb_jnt3Transform = vtk.vtkTransform()
    thumb_jnt3Transform.SetInput(thumb_jnt2Transform)

    thumb_jnt3Actor.SetUserTransform(thumb_jnt3Transform)
    thumb_jnt3Actor.SetMapper(thumb_jnt3Mapper)
    thumb_jnt3Actor.SetObjectName('thumb_jnt3')
    thumb_jnt3Actor.GetProperty().SetColor(colors.GetColor3d('Grey'))

    thumb2Pos = thumb2Actor.GetPosition()
    thumb_jnt3Actor.SetPosition(thumb2Pos[0],
                          thumb2Pos[1] + thumb2.GetHeight() / 2 + thumb_jnt3.GetRadius() * 0.75,
                          thumb2Pos[2])


    # ====================================== finger3 ======================================

    # index3
    index3 = vtkCylinderSource()
    index3.SetRadius(1.5)
    index3.SetHeight(2)
    index3.SetResolution(20)

    index3Mapper = vtkPolyDataMapper()
    index3Mapper.SetInputConnection(index3.GetOutputPort())

    index3Actor = vtkActor()
    index3Actor.SetUserTransform(index_jnt3Transform)
    index3Actor.SetMapper(index3Mapper)
    index3Actor.GetProperty().SetColor(colors.GetColor3d("RoyalBLue"))

    index_jnt3Pos = index_jnt3Actor.GetPosition()
    index3Actor.SetPosition(index_jnt3Pos[0],
                         index_jnt3Pos[1] + index_jnt3.GetRadius() / 2 + index3.GetHeight() / 2,
                         index_jnt3Pos[2])

    # middle3
    middle3 = vtkCylinderSource()
    middle3.SetRadius(1.5)
    middle3.SetHeight(2)
    middle3.SetResolution(20)

    middle3Mapper = vtkPolyDataMapper()
    middle3Mapper.SetInputConnection(middle3.GetOutputPort())

    middle3Actor = vtkActor()
    middle3Actor.SetUserTransform(middle_jnt3Transform)
    middle3Actor.SetMapper(middle3Mapper)
    middle3Actor.GetProperty().SetColor(colors.GetColor3d("RoyalBLue"))

    middle_jnt3Pos = middle_jnt3Actor.GetPosition()
    middle3Actor.SetPosition(middle_jnt3Pos[0],
                      middle_jnt3Pos[1] + middle_jnt3.GetRadius() / 2 + middle3.GetHeight() / 2,
                      middle_jnt3Pos[2])

    # ring3
    ring3 = vtkCylinderSource()
    ring3.SetRadius(1.5)
    ring3.SetHeight(2)
    ring3.SetResolution(20)

    ring3Mapper = vtkPolyDataMapper()
    ring3Mapper.SetInputConnection(ring3.GetOutputPort())

    ring3Actor = vtkActor()
    ring3Actor.SetUserTransform(ring_jnt3Transform)
    ring3Actor.SetMapper(ring3Mapper)
    ring3Actor.GetProperty().SetColor(colors.GetColor3d("RoyalBLue"))

    ring_jnt3Pos = ring_jnt3Actor.GetPosition()
    ring3Actor.SetPosition(ring_jnt3Pos[0],
                           ring_jnt3Pos[1] + ring_jnt3.GetRadius() / 2 + ring3.GetHeight() / 2,
                           ring_jnt3Pos[2])

    # pinky3
    pinky3 = vtkCylinderSource()
    pinky3.SetRadius(1.5)
    pinky3.SetHeight(2)
    pinky3.SetResolution(20)

    pinky3Mapper = vtkPolyDataMapper()
    pinky3Mapper.SetInputConnection(pinky3.GetOutputPort())

    pinky3Actor = vtkActor()
    pinky3Actor.SetUserTransform(pinky_jnt3Transform)
    pinky3Actor.SetMapper(pinky3Mapper)
    pinky3Actor.GetProperty().SetColor(colors.GetColor3d("RoyalBLue"))

    pinky_jnt3Pos = pinky_jnt3Actor.GetPosition()
    pinky3Actor.SetPosition(pinky_jnt3Pos[0],
                          pinky_jnt3Pos[1] + pinky_jnt3.GetRadius() / 2 + pinky3.GetHeight() / 2,
                          pinky_jnt3Pos[2])

    # thumb3
    thumb3 = vtkCylinderSource()
    thumb3.SetRadius(1.5)
    thumb3.SetHeight(2)
    thumb3.SetResolution(20)

    thumb3Mapper = vtkPolyDataMapper()
    thumb3Mapper.SetInputConnection(thumb3.GetOutputPort())

    thumb3Actor = vtkActor()
    thumb3Actor.SetUserTransform(thumb_jnt3Transform)
    thumb3Actor.SetMapper(thumb3Mapper)
    thumb3Actor.GetProperty().SetColor(colors.GetColor3d("RoyalBLue"))

    thumb_jnt3Pos = thumb_jnt3Actor.GetPosition()
    thumb3Actor.SetPosition(thumb_jnt3Pos[0],
                          thumb_jnt3Pos[1] + thumb_jnt3.GetRadius() / 2 + thumb3.GetHeight() / 2,
                          thumb_jnt3Pos[2])

    # ==================================== finger_tip ====================================

    # index_tip
    index_tip = vtkSphereSource()
    index_tip.SetRadius(1.5)
    index_tip.SetPhiResolution(20)
    index_tip.SetThetaResolution(20)

    index_tipMapper = vtkPolyDataMapper()
    index_tipMapper.SetInputConnection(index_tip.GetOutputPort())

    index_tipActor = vtkActor()
    index_tipActor.SetUserTransform(index_jnt3Transform)
    index_tipActor.SetMapper(index_tipMapper)
    index_tipActor.GetProperty().SetColor(colors.GetColor3d('RoyalBLue'))

    index3Pos = index3Actor.GetPosition()
    index_tipActor.SetPosition(index3Pos[0],
                               index3Pos[1] + index3.GetHeight() / 2,
                               index3Pos[2])

    # middle_tip
    middle_tip = vtkSphereSource()
    middle_tip.SetRadius(1.5)
    middle_tip.SetPhiResolution(20)
    middle_tip.SetThetaResolution(20)

    middle_tipMapper = vtkPolyDataMapper()
    middle_tipMapper.SetInputConnection(middle_tip.GetOutputPort())

    middle_tipActor = vtkActor()
    middle_tipActor.SetUserTransform(middle_jnt3Transform)
    middle_tipActor.SetMapper(middle_tipMapper)
    middle_tipActor.GetProperty().SetColor(colors.GetColor3d('RoyalBLue'))

    middle3Pos = middle3Actor.GetPosition()
    middle_tipActor.SetPosition(middle3Pos[0],
                                middle3Pos[1] + middle3.GetHeight() / 2,
                                middle3Pos[2])

    # ring_tip
    ring_tip = vtkSphereSource()
    ring_tip.SetRadius(1.5)
    ring_tip.SetPhiResolution(20)
    ring_tip.SetThetaResolution(20)

    ring_tipMapper = vtkPolyDataMapper()
    ring_tipMapper.SetInputConnection(ring_tip.GetOutputPort())

    ring_tipActor = vtkActor()
    ring_tipActor.SetUserTransform(ring_jnt3Transform)
    ring_tipActor.SetMapper(ring_tipMapper)
    ring_tipActor.GetProperty().SetColor(colors.GetColor3d('RoyalBLue'))

    ring3Pos = ring3Actor.GetPosition()
    ring_tipActor.SetPosition(ring3Pos[0],
                              ring3Pos[1] + ring3.GetHeight() / 2,
                              ring3Pos[2])

    # pinky_tip
    pinky_tip = vtkSphereSource()
    pinky_tip.SetRadius(1.5)
    pinky_tip.SetPhiResolution(20)
    pinky_tip.SetThetaResolution(20)

    pinky_tipMapper = vtkPolyDataMapper()
    pinky_tipMapper.SetInputConnection(pinky_tip.GetOutputPort())

    pinky_tipActor = vtkActor()
    pinky_tipActor.SetUserTransform(pinky_jnt3Transform)
    pinky_tipActor.SetMapper(pinky_tipMapper)
    pinky_tipActor.GetProperty().SetColor(colors.GetColor3d('RoyalBLue'))

    pinky3Pos = pinky3Actor.GetPosition()
    pinky_tipActor.SetPosition(pinky3Pos[0],
                               pinky3Pos[1] + pinky3.GetHeight() / 2,
                               pinky3Pos[2])
    
    # thumb_tip
    thumb_tip = vtkSphereSource()
    thumb_tip.SetRadius(1.5)
    thumb_tip.SetPhiResolution(20)
    thumb_tip.SetThetaResolution(20)

    thumb_tipMapper = vtkPolyDataMapper()
    thumb_tipMapper.SetInputConnection(thumb_tip.GetOutputPort())

    thumb_tipActor = vtkActor()
    thumb_tipActor.SetUserTransform(thumb_jnt3Transform)
    thumb_tipActor.SetMapper(thumb_tipMapper)
    thumb_tipActor.GetProperty().SetColor(colors.GetColor3d('RoyalBLue'))

    thumb3Pos = thumb3Actor.GetPosition()
    thumb_tipActor.SetPosition(thumb3Pos[0],
                               thumb3Pos[1] + thumb3.GetHeight() / 2,
                               thumb3Pos[2])

    # renderer.AddActor(palmActor)
    renderer.AddActor(carpal1Actor)
    renderer.AddActor(carpal2Actor)
    renderer.AddActor(carpal3Actor)
    renderer.AddActor(carpal4Actor)
    renderer.AddActor(carpal0Actor)
    renderer.AddActor(wrist_jntActor)
    #---------------------------------#
    renderer.AddActor(index_jnt1Actor)
    renderer.AddActor(middle_jnt1Actor)
    renderer.AddActor(ring_jnt1Actor)
    renderer.AddActor(pinky_jnt1Actor)
    renderer.AddActor(thumb_jnt1Actor)
    #---------------------------------#
    renderer.AddActor(index1Actor)
    renderer.AddActor(middle1Actor)
    renderer.AddActor(ring1Actor)
    renderer.AddActor(pinky1Actor)
    renderer.AddActor(thumb1Actor)
    #---------------------------------#
    renderer.AddActor(index_jnt2Actor)
    renderer.AddActor(middle_jnt2Actor)
    renderer.AddActor(ring_jnt2Actor)
    renderer.AddActor(pinky_jnt2Actor)
    renderer.AddActor(thumb_jnt2Actor)
    #---------------------------------#
    renderer.AddActor(index2Actor)
    renderer.AddActor(middle2Actor)
    renderer.AddActor(ring2Actor)
    renderer.AddActor(pinky2Actor)
    renderer.AddActor(thumb2Actor)
    #---------------------------------#
    renderer.AddActor(index_jnt3Actor)
    renderer.AddActor(middle_jnt3Actor)
    renderer.AddActor(ring_jnt3Actor)
    renderer.AddActor(pinky_jnt3Actor)
    renderer.AddActor(thumb_jnt3Actor)
    #---------------------------------#
    renderer.AddActor(index3Actor)
    renderer.AddActor(middle3Actor)
    renderer.AddActor(ring3Actor)
    renderer.AddActor(pinky3Actor)
    renderer.AddActor(thumb3Actor)
    #---------------------------------#
    renderer.AddActor(index_tipActor)
    renderer.AddActor(middle_tipActor)
    renderer.AddActor(ring_tipActor)
    renderer.AddActor(pinky_tipActor)
    renderer.AddActor(thumb_tipActor)


    interactor.Initialize()
    renwin.Render()
    interactor.Start()

if __name__ == '__main__':
    main()

