package main



import (
	"fmt"
	"io/ioutil"
	"net/http"
	"strings"
	"regexp"
	"strconv"
	"sort"
)




func get_channel_from_reddit() {
	fmt.Println("hello")
}

type Paste struct {
	key string
	date int
	title string
	size int
	expire_date int
	private int
	format_long string
	format_short string
	url string
	hits int
} 

type Pastelist []*Paste

func get_channel_from_pastebin(uuid string) string {
	api_dev_key 		:= "HfvXu-FGu_kXfA2T1sGL_bL_nKVSkQpz"
	api_user_key 		:= "36686b07556044d040f059205f73956e"
	api_results_limit 	:= "100"
	api_post_url 		:= "https://pastebin.com/api/api_post.php"
	api_raw_url 		:= "https://pastebin.com/api/api_raw.php";

	data := strings.NewReader("api_option=list&api_user_key="+api_user_key+"&api_dev_key="+api_dev_key+"&api_results_limit="+api_results_limit)
	resp, err := http.Post(api_post_url,"application/x-www-form-urlencoded",data)
	if err != nil {
		fmt.Println(err)
	}

	defer resp.Body.Close()
	body, err := ioutil.ReadAll(resp.Body)
	if err != nil {
		fmt.Println(err)
	}

	// fmt.Println(string(body))

	// body := 
	// `<paste>
	// <paste_key>dMNKeqF3</paste_key>
	// <paste_date>1598339635</paste_date>
	// <paste_title>test280ec4</paste_title>
	// <paste_size>378</paste_size>
	// <paste_expire_date>1598944435</paste_expire_date>
	// <paste_private>0</paste_private>
	// <paste_format_long>None</paste_format_long>
	// <paste_format_short>text</paste_format_short>
	// <paste_url>https://pastebin.com/dMNKeqF3</paste_url>
	// <paste_hits>4</paste_hits>
	// </paste>
	// <paste>
	// <paste_key>dMNKeqF3</paste_key>
	// <paste_date>1598339636</paste_date>
	// <paste_title>test280ec4</paste_title>
	// <paste_size>378</paste_size>
	// <paste_expire_date>1598944435</paste_expire_date>
	// <paste_private>0</paste_private>
	// <paste_format_long>None</paste_format_long>
	// <paste_format_short>text</paste_format_short>
	// <paste_url>https://pastebin.com/dMNKeqF3</paste_url>
	// <paste_hits>4</paste_hits>
	// </paste>`

	var list []*Paste

	reg_paste := regexp.MustCompile(`<paste>(?s).*?</paste>`)
	result := reg_paste.FindAllStringSubmatch(string(body),-1)
	num_paste := len(result)
	reg_paste_detail := regexp.MustCompile(`<paste_.*?>(.*?)</paste_.*?>`)
	for i := 0; i < num_paste; i++ {
		// fmt.Println(result[i][0])
		result_detail := reg_paste_detail.FindAllStringSubmatch(result[i][0],-1)
		key := result_detail[0][1]
		date,err := strconv.Atoi(result_detail[1][1])
		if err != nil {
			fmt.Println(err)
		}
		title := result_detail[2][1]
		size,err := strconv.Atoi(result_detail[3][1])
		if err != nil {
			fmt.Println(err)
		}
		expire_date,err := strconv.Atoi(result_detail[4][1])
		if err != nil {
			fmt.Println(err)
		}
		private,err := strconv.Atoi(result_detail[5][1])
		if err != nil {
			fmt.Println(err)
		}
		format_long := result_detail[6][1]
		format_short := result_detail[7][1]
		url := result_detail[8][1]
		hits,err := strconv.Atoi(result_detail[9][1])
		if err != nil {
			fmt.Println(err)
		}
		paste_detail := Paste{
			key:key,
			date:date,
			title:title,
			size:size,
			expire_date:expire_date,
			private:private,
			format_long:format_long,
			format_short:format_short,
			url:url,
			hits:hits}
		// fmt.Println(paste_detail)
		match_uuid := strings.HasSuffix(paste_detail.title, uuid[len(uuid)-6:])
		if match_uuid{
			list = append(list, &paste_detail)
		}
	}
	if len(list)== 0 {
		return("uuid not match any post")
	}else{
		sort.Sort(Pastelist(list))  //调用标准库的sort.Sort必需要先实现Len(),Less(),Swap() 三个方法.
		// for _, v := range list {
		// 	fmt.Println("key：", v.key, "date：", v.date,"title：", v.title)
		// }
		// pastebin_key
		// fmt.Println(list[0].key)

		data_raw := strings.NewReader("api_option=show_paste&api_user_key="+api_user_key+"&api_dev_key="+api_dev_key+"&api_paste_key="+list[0].key)
		resp_raw, err := http.Post(api_raw_url,"application/x-www-form-urlencoded",data_raw)
		if err != nil {
			fmt.Println(err)
		}

		defer resp_raw.Body.Close()
		body_raw, err := ioutil.ReadAll(resp_raw.Body)
		if err != nil {
			fmt.Println(err)
		}
		// fmt.Println(string(body_raw))
		return string(body_raw)
	}
	
}

func (I Pastelist) Len() int {
	return len(I)
}
func (I Pastelist) Less(i, j int) bool {
	return I[i].date > I[j].date
}
func (I Pastelist) Swap(i, j int) {
	I[i], I[j] = I[j], I[i]
}

func get_channel_from_sms() {
	fmt.Println("hello")
}

func aes_decrypt(data string,uuid string){
	fmt.Println(data)
	fmt.Println(uuid)
}

func get_channel_info(channel_type string, param []string){
	fmt.Println("hello")
}

func main() {
	uuid := "0126fb76-e6a2-11ea-9028-000c29280ec4"
	pastebin_data := get_channel_from_pastebin(uuid)
	fmt.Println(pastebin_data)
}