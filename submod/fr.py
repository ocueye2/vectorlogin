import anki_vector
from anki_vector.util import degrees
import threading, time
import sys
from PIL import Image
import os
os.chdir("/home/ocueye/Documents/workspace/docker/vector/vectorlogin/submod")
import lights
import dotenv
os.chdir("/home/ocueye/Documents/workspace/docker/vector/vectorlogin")
dotenv.load_dotenv()

setscene = lights.HomeAssistantScenes(os.getenv("hassurl"),os.getenv("token"))

def showimage(path,robot):
    current_directory = os.path.dirname(os.path.realpath(__file__))
    image_path = os.path.join(current_directory, "..", path)
        # Load an image
    image_file = Image.open(image_path)

    screen_data = anki_vector.screen.convert_image_to_screen_data(image_file)

    duration_s = 1.0
    robot.screen.set_screen_with_image_data(screen_data, duration_s)
    robot.screen.set_screen_with_image_data(screen_data, duration_s)


def checkuser():
    global found

    found = ""

    def on_robot_observed_face(robot, event_type, event, evt):
        if event:
            global found
            name = event.name or "stranger"
            print(f"saw {name}")
            found = name
            evt.set()

    with anki_vector.Robot(enable_face_detection=True) as robot:
        robot.behavior.drive_on_charger();
        robot.behavior.drive_off_charger()
        # If necessary, adjust Vector's head and lift to make it easier to see his face
        setscene.activate("scan-init")
        robot.behavior.turn_in_place(degrees(20))
        robot.behavior.set_head_angle(degrees(20.0))
        robot.behavior.set_lift_height(0.0)
        showimage("image/scan.png",robot)
        robot.audio.stream_wav_file("image/sfx/scan.wav", 75)
        time.sleep(1)
        evt = threading.Event()
        robot.events.subscribe(on_robot_observed_face, anki_vector.events.Events.robot_observed_face, evt)

        print("------ waiting for face events, press ctrl+c to exit early ------")

        try:
            if not evt.wait(timeout=5):
                print("------ Vector never saw your face! ------")
        except KeyboardInterrupt:
            pass

        
        robot.events.unsubscribe(on_robot_observed_face, anki_vector.events.Events.robot_observed_face)
        if found == "ocu eye":
            setscene.activate("scan-suc")
            showimage("image/suc.png",robot)
            robot.audio.stream_wav_file("image/sfx/suc.wav", 75)
            robot.behavior.say_text(f"well come ocu eye")
            robot.behavior.turn_in_place(degrees(160))
            robot.behavior.drive_on_charger()
            setscene.activate("light")
            return True
        else:
            setscene.activate("scan-suc")
            showimage("image/fail.png",robot)
            robot.audio.stream_wav_file("image/sfx/fail.wav", 75)
            robot.behavior.say_text(f"{found} you are not authorised")
            robot.behavior.turn_in_place(degrees(160))
            robot.behavior.drive_on_charger()
            setscene.activate("light")
            return False
        

if __name__ == "__main__":
    checkuser()
