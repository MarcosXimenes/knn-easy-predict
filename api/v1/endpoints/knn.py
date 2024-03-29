from fastapi import APIRouter, UploadFile, Form
from libraries import helper
from fastapi.responses import FileResponse

router = APIRouter()


@router.post("/train")
@router.post("/train/", include_in_schema=False)
async def training_and_return_mc(
    keyword: str = Form(), neighbors: int = Form(), file: UploadFile = Form()
):
    contents = file.file.read()
    df = helper.file_to_df(contents)
    file.file.close()

    new_cols = [col for col in df.columns if col != str(keyword)] + [str(keyword)]
    df = df[new_cols]
    df = df.dropna()
    df = df._get_numeric_data()

    train, test = helper.train_test_split(df, keyword)

    real, predicts = helper.predict(train, test, neighbors)

    helper.create_confusion_matrix(real, predicts)

    return FileResponse("confusion_matrix.png")
