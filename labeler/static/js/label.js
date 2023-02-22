const imageContainer = document.getElementById("label-container");
const rectangleBtn = document.getElementById("rectangle");
const annotateModal = new bootstrap.Modal(document.getElementById("label-info-modal"));
const dataSaver = document.getElementById("data-saver");
const b64Media = imageContainer.dataset.media;

const finalForm = document.getElementById("final-form");

const stage = new Konva.Stage({
    container: 'label-container',
    height: 700,
    width: 1080
})

const layer = new Konva.Layer();

stage.add(layer);

const imageObj = new Image();
imageObj.onload = () => {
    const imageLayer = new Konva.Image({
        image: imageObj,
        width: stage.getWidth(),
        height: stage.getHeight()
    });
    layer.add(imageLayer)
}
imageObj.src = `data:image/jpeg;base64,${b64Media}`;


stage.add(layer)


rectangleBtn.addEventListener('click', (clickEvent) => {
    annotateModal.show("label-info-modal");
    const annotateButton = document.getElementById("annotate");
    annotateButton.addEventListener('click', (_) => {
        const labelForm = document.getElementById("labelForm");
        const form = new FormData(labelForm);
        const annotateObj = Object.fromEntries(form.entries());
        dataSaver.setAttribute("data-annotate", annotateObj.labelContent);
        annotateModal.hide("label-info-modal");
    })
});

document.addEventListener('hidden.bs.modal', (event) => {
    const rect = new Konva.Rect({
        x: stage.getWidth() / 2,
        y: stage.getHeight() / 2,
        width: 200,
        height: 200,
        cornerRadius: 3,
        drawBorder: true,
        stroke: "black",
        strokeWidth: 20,
        // fill: "black",
        name: dataSaver.dataset.annotate,
        draggable: true,
    });
    layer.add(rect);
    rect.on('mouseout', () => {
        const {x, y} = rect.getPosition();
        dataSaver.setAttribute("data-pos-x", x);
        dataSaver.setAttribute("data-pos-y", y);
    })
})


finalForm.addEventListener('submit', (event) => {
    event.preventDefault();
    const form = new FormData(event.target);
    const obj = Object.fromEntries(form.entries());
    const comments = String(obj.comments);
    const userId = String(obj.userId);
    const dataSaverInfo = dataSaver.dataset;
    const apiPath = dataSaverInfo.apiUrl;
    delete dataSaverInfo.apiUrl;
    if (!dataSaverInfo) {
        return
    }
    const labellingData = {...dataSaverInfo, comments, userId};
    const url = `${window.location.protocol}//${window.location.host}${apiPath}`
    fetch(url, {
        headers: {
            "Content-Type": "application/json",
            "Accept": "*/*"
        },
        body: JSON.stringify(labellingData),
        method: "POST"
    }).then((res) => res.text())
        .then(data => {
            const resObj = JSON.parse(data);
            window.location.href = resObj.redirectPath;
        })
})


