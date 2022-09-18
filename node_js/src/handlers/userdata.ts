import express, { Application } from 'express';
import {Request,Response} from 'express';
import multer from 'multer';
import app from '../server';
// import fetch from "node-fetch";

const fetch = require("cross-fetch");

// const request = require("request");


let arr:string[] = [];

var storage = multer.diskStorage({
     destination:function(req, file, cb) {
      cb(null, './uploads')
    },
    filename: function (req, file, cb) {
      cb(null,file.originalname)
       
    }
})

var upload = multer({ storage: storage })

const userRoute = (app:express.Application)=>{
    app.post('/upload_data',upload.array("files"), userData);

    // app.post('http://localhost:5000/upload_data', upload.array("files"), );
}


interface MulterRequest extends Request {
    files: any;
}


const userData = async (req:Request, res:Response)=>{

    arr = []
    console.log(req.body.li);
    //console.log((req as MulterRequest).files);
    let values = (req as MulterRequest).files
    for(let i=0;i<values.length;i++){
        arr.push(values[i]['filename']);
    }
    console.log(arr);

    let license_num = req.body.li
    
    // req.body["files"] = arr


    const response_ = await fetch("http://localhost:5000/upload_data", {
        method: "POST",
        headers: {
          Accept: "application/json",
          "Content-Type": "application/json",
        },
        body: JSON.stringify({"li": license_num,"files":arr}
        ),
      });
    
      console.log(await response_.json())
      res.json({ message: "Successfully uploaded files" });
    
      

    // // block 1
    

    // // app.post("http://localhost:5000/upload_data", {"path": "car.jpg"})
    // request("http://localhost:5000/upload_data", function (response:Response, body:object) {

    //     res.send(body)
    // })

    // *****************************************************

    // 

    // req.files.forEach((f, i) => {
    //     fs.renameSync(f.path, `uploads/${req.body.li}_${i}.jpg`, (err) => {
    //       if (err) throw err;
    //     });
    //   });
    
    //   await fetch("http://localhost:3001/upload_data", {
    //     method: "GET",
    //     body: JSON.stringify({
    //       files: req.files.map((f, i) => {
    //         return `${req.body.li}_${i}.jpg`;
    //       }),
    //     }),
    //   }).catch((err) => {
    //     res.send(err);
    //   });
    
}
    
    
    
// another code sent
// const formData = new FormData();
//   formData.append("files", req.files);
//   formData.append("li", req.body.li);
//   await fetch("http://localhost:3001/upload_data", {
//     method: "POST",
//     body: formData,
//   }).catch((err) => {
//     res.send(err);
//   });

//   console.log(req);
//   req.files.forEach((f, i) => {
//     fs.renameSync(f.path, `uploads/${req.body.li}_${i}.jpg`, (err) => {
//       if (err) throw err;
//     });
//   });





const dataToModel = (req:Request,res:Response)=>{
    
}

export default userRoute;