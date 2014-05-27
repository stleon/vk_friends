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
        if (req) {
            common_friends = common_friends + [req];
        }
        else {
            common_friends = common_friends + [0];
        }
        parametr = "";
    }
    start = start + 1;
}
return common_friends;