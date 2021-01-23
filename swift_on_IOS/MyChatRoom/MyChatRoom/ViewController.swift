//
//  ViewController.swift
//  MyChatRoom
//
//  Created by ESD 14 on 2020/12/24.
//  Copyright © 2020年 ESD 14. All rights reserved.
//

import UIKit

class ViewController: UIViewController {
    @IBOutlet weak var messageTextField: UITextField!
    @IBOutlet weak var chatContentTextView: UITextView!
    var cnt = 0
    override func viewDidLoad() {
        super.viewDidLoad()
        // Do any additional setup after loading the view, typically from a nib.
    }

    override func didReceiveMemoryWarning() {
        super.didReceiveMemoryWarning()
        // Dispose of any resources that can be recreated.
    }
    
}

