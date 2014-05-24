var source = Args.source;
var targets = Args.targets;

var common_friends = {};

var req;

var parametr = "";
var start = 0;

// из строки с целями вынимаем каждую цель
while(start<=targets.length-1){
    if (targets.substr(start, 1) != "," && start != targets.length-1){
        parametr = parametr + targets.substr(start, 1);
    }
    else {
        // сразу делаем запросы, как только вытащили id
        req = API.friends.getMutual({"source_uid":source, "target_uid":parametr});
        // а нужно common_friends[parametr] = req;
        //parametr = parseInt(parametr);
        common_friends = common_friends + {parametr: req};
        parametr = "";
    }
    start = start + 1;
}
var a = {"cname":456};
a = a + {"name":123, "lol":76478167};
var test = "123";
//a[test] = 222;
a = a + {test: 222};
//a["a"] = 213;
return a;