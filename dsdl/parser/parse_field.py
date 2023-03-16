
import re
from dataclasses import dataclass
from typing import Optional, Set, Dict
from typing import List as _List

# �ȵ���dsdl.fields����FIELD�ſ�����Ч
from dsdl.fields import *
from dsdl.geometry import FIELD
from dsdl.exception import DefineSyntaxError
from .utils import *

@dataclass()
class EleStruct:
    name: str
    type: str


class ParserField():
    def __init__(self,
                    struct_name_params: Dict,
                    struct_name: Set[str], 
                    struct_params: str = None):
        self.struct_name_params = struct_name_params # ����struct��params������У��cdom��
        self.struct = struct_name  # field �а�����struct������У����
        self.struct_params = struct_params
    
    def pre_parse_struct_field(
        self, field_name: Optional[str], raw_field_type: str
    ) -> str:
        """
        У��struct���͵�ÿ���ֶε���ں������Բ�ͬ�����Int,Image,List...�����ֶν���У�鲢�����ڴ档
            field_name: like: "category_id", "category", "annotation", None, ....
            raw_field_type: like: Int, Label[dom=$cdom0], List[List[Int], ordered = True], 'dom=$cdom0', ....
        """
        # Image->Image(), List[KeyPointLocalObject] -> List(KeyPointLocalObject())
        # List[etype=KeyPointLocalObject[cdom0=$cdom0]] -> List(etype=KeyPointLocalObject(cdom0=$cdom0))
        raw_field_type = raw_field_type.strip()
        fixed_params = re.findall(r"\[(.*)\]", raw_field_type)
        if len(fixed_params)==0:
           field_type = self.parse_type(raw_field_type)
        else:
            k_v_list_ori = fixed_params[0]
            raplace_field_type = raw_field_type.replace("[" + k_v_list_ori + "]", "")
            # below can split 'etype=LocalObjectEntry[cdom=COCO2017ClassDom, optional=True], optional=True' to
            # ['etype=LocalObjectEntry[cdom=COCO2017ClassDom', 'optional=True]', 'optional=True'],����ԭ��˳��
            k_v_list_ori = re.split(r",\s*(?![^\[]*\])", k_v_list_ori)
            k_v_list = list(set([i.strip() for i in k_v_list_ori]))
            k_v_list.sort(key = k_v_list_ori.index)
            new_list = []

            for k_v in k_v_list:
                # k_v_temp = k_v.replace(" ", "")
                if not check_is_bracket_pair(k_v):
                    raise DefineSyntaxError(
                        f"Error in field with value of `{raw_field_type}`. Check the `{k_v}` part."
                    )
                if raplace_field_type in self.struct:
                    # �ж�cdom,�͵���struct��params��Ӧ
                    k =  k_v.split('=')[0]
                    if k in self.struct_name_params[raplace_field_type]:
                        
                        if len(k_v.split('='))<2:
                            raise DefineSyntaxError( f"{k_v} is {raplace_field_type} params, should have '='")
                        cdom_name =  k_v.split('=')[1] 
                
                        # У��cdom_name�Ƿ���϶���
                        if cdom_name.replace('$','') not in self.struct_params:
                            raise DefineSyntaxError(
                                    f"definition error of dom '{cdom_name}' not in $params `{self.struct_params}`, "
                                    f"check cdom is defined correctly."
                                )
                        cdom_name = '"' + cdom_name + '"'
                        k_v =  k_v.replace( k_v.split('=')[1], cdom_name)
                elif k_v.startswith(('dom','cdom')):
                    k = k_v.split('=')[0]
                    if len(k_v.split('='))<2:
                        raise DefineSyntaxError( f"{k_v} is {raplace_field_type} params, should have '='")
                    cdom_name =  k_v.split('=')[1] 
                    if cdom_name.replace('$','') not in self.struct_params:
                        raise DefineSyntaxError(
                                    f"definition error of dom '{cdom_name}' not in $params `{self.struct_params}`, "
                                    f"check cdom is defined correctly."
                                )
                    cdom_name = '"' + cdom_name + '"'
                    k_v =  k_v.replace( k_v.split('=')[1], cdom_name)

                new_list.append(k_v)

            field_type = self.parse_type(raplace_field_type, new_list)
        return field_type

    
    def parse_type(
        self,
        field_type: str,
        param_list: _List[str] = None,
        ) -> str:
        """
        У�����type���γ�.py��Ҫ��ʽ��
        field_type: like: Int, Label, List,  'dom=$cdom0', ....
        param_list: like: None, ['dom=$cdom0'], ['List[Int]', 'ordered = True'], None, ....
        """
        if field_type.startswith('List'):
            field_type = self.parse_list_field(field_type,param_list)
            return field_type
        # ��List��ͷ����ʱ������Ƕ�׵����
        else:
            params_str = ''
            # eg. optional=True, cdom=$cdom, BBox,
            # -------------------------------------------------------------������fieldlist���ж�,����Ӹ�ʽ�ж�
            if field_type in FIELD or field_type in self.struct:
                check_name_format(field_type)
                # ����param
                if param_list:
                    for param in param_list:
                        # eg. optional=True, cdom=$cdom, BBox, NewType[is_optional=True]
                        param_str = self.pre_parse_struct_field(field_name=None,raw_field_type=param)
                        params_str += (param_str + ',')
                    params_str = params_str[:-1]
                return field_type + '(' + params_str + ')'
            else:
                if param_list:
                    raise DefineSyntaxError(f'definition error of {field_type} has {param_list}, please check field ')
                
                if field_type.split('=')[-1]=='true':
                    field_type = field_type.replace(field_type.split('=')[-1],'True')
                if field_type.split('=')[-1]=='false':
                    field_type = field_type.replace(field_type.split('=')[-1],'False')
                return field_type
            

    def parse_list_field(self, 
                         field_type: str, 
                         param_list: _List[str]
                         ) -> str:
        """
        ��������List���͵�field
        """
        # field_type:List
        # param_list:[etype=KeyPointLocalObject[cdom0=$cdom0],ordered=True] or Bbox
        # ���ﲻ����etypeʶ����ʲôתʲô,ʶ�𵽵�struct��Ҫ��ʽ����Ϊetype=xxx
        res = field_type + "("
        if param_list:
            for param in param_list:
                if param.startswith('etype'):
                    ele_type_name = param.split("=",1)[0].strip()
                    if len(param.split("=",1))<2:
                        raise DefineSyntaxError( f"{param} is list etype params, should have '='")
                    ele_type = param.split("=",1)[1].strip()

                    ele_type = self.pre_parse_struct_field(field_name=None, raw_field_type=ele_type)
                    res += (ele_type_name + "=" + ele_type + ',')
                else:
                    ele_type = self.pre_parse_struct_field(field_name=None, raw_field_type=param)
                    res += (ele_type+ ',')
            res = res[:-1]
            
        return res + ')'