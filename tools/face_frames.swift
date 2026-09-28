import Foundation
import Vision
import AppKit

for path in CommandLine.arguments.dropFirst() {
    guard let img = NSImage(contentsOfFile: path),
          let cg = img.cgImage(forProposedRect: nil, context: nil, hints: nil) else {
        print("\(path)\t-1\t0"); continue
    }
    let req = VNDetectFaceRectanglesRequest()
    try? VNImageRequestHandler(cgImage: cg, options: [:]).perform([req])
    let faces = req.results ?? []
    // biggest face as a share of frame height — a presenter fills the frame,
    // a face inside a screenshot does not
    let biggest = faces.map { $0.boundingBox.height }.max() ?? 0
    print("\(path)\t\(faces.count)\t\(String(format: "%.3f", biggest))")
}
