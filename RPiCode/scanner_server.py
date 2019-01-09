import socketserver
import picamera
import argparse
import time

class ScannerRequestHandler(socketserver.BaseRequestHandler):

    def handle(self):
        print("Scan requested by %s" % self.client_address[0])
        scan_label = "scan_%03d" % self.server.counter
        scan = self.make_scan(scan_label)
        with open(scan, "rb") as scan_data:
            self.request.sendall(scan_data.read())
        server.increment_counter()

    def make_scan(self, scan_lab):
        return self.server.make_scan(scan_lab)


class ScannerServer(socketserver.TCPServer):

    def __init__(self, server_address, RequestHandlerClass, img_dir, counter=0):
        super().__init__(server_address, RequestHandlerClass)
        self.dir = img_dir
        self.counter = counter
        self.camera = picamera.PiCamera()

    def increment_counter(self):
        self.counter += 1
        with open("counter", "w") as count_file:
            count_file.write(self.counter)


    def make_scan(self, scan_label):
        scan_full_path = "%s/%s.jpg" % (self.dir, scan_label)
        self.camera.start_preview()
        time.sleep(5)
        self.camera.capture(scan_full_path)
        self.camera.stop_preview()
        return scan_full_path


def parse_cl_args():
        parser = argparse.ArgumentParser("Program to allow a Raspberry Pi with camera to behave like a scanner, taking a picture and passing it to the client when it receives a request")
        parser.add_argument("host", type=str, help="IP address for the host.")
        parser.add_argument("port", type=int, default=1200, help="Port number to be used (should be > 1023)")
        parser.add_argument("path", type=str, help="Path to directory where scanned images should be saved.")
        parser.add_argument("counter", type=int, default=0, help="Int for tracking how many images have been captured (default is 0).")

        args = parser.parse_args()

        return args.host, args.port, args.path, args.counter


if __name__ == "__main__":

    host, port, path, counter = parse_cl_args()

    server = ScannerServer((host, port), ScannerRequestHandler, path, counter)
    server.serve_forever()
