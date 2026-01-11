<template>
   <div v-if="editor" class="editor-container">
      
      <div class="editor-menu editorbutton-group">

         <button class="editorbutton" 
               @click="editor.chain().focus().toggleBold().run()" 
               :disabled="!editor.can().chain().focus().toggleBold().run()" 
               :class="{ 'is-active': editor.isActive('bold') }" 
               title="Жирный текст"
               type="button">
            <i class="fa-solid fa-bold"></i>
         </button>
         <button class="editorbutton" 
               @click="editor.chain().focus().toggleItalic().run()" 
               :disabled="!editor.can().chain().focus().toggleItalic().run()" 
               :class="{ 'is-active': editor.isActive('italic') }" 
               title="Курсив"
               type="button">
            <i class="fa-solid fa-italic"></i>
         </button>
         <button class="editorbutton" 
               @click="editor.chain().focus().toggleStrike().run()" 
               :disabled="!editor.can().chain().focus().toggleStrike().run()" 
               :class="{ 'is-active': editor.isActive('strike') }" 
               title="Зачеркнутый текст"
               type="button">
            <i class="fa-solid fa-strikethrough"></i>
         </button>
         <button class="editorbutton" 
               @click="editor.chain().focus().toggleUnderline().run()" 
               :disabled="!editor.can().toggleUnderline()" 
               :class="{ 'is-active': editor.isActive('underline') }" 
               title="Подчеркнутый текст"
               type="button">
            <i class="fa-solid fa-underline"></i>
         </button>
         <button class="editorbutton" 
               @click="editor.chain().focus().toggleHighlight().run()" 
               :class="{ 'is-active': editor.isActive('highlight') }" 
               title="Выделить текст"
               type="button">
            <i class="fa-solid fa-highlighter"></i>
         </button>
         <button class="editorbutton"
               @click="editor.chain().focus().unsetAllMarks().run()" 
               title="Очистить форматирование"
               type="button">
            <i class="fa-solid fa-eraser"></i>
         </button>

         <button class="editorbutton" 
               @click="editor.chain().focus().setTextAlign('left').run()" 
               :class="{ 'is-active': editor.isActive({ textAlign: 'left' }) }" 
               title="Выравнивание по левому краю"
               type="button">
            <i class="fa-solid fa-align-left"></i>
         </button>
         <button class="editorbutton" 
               @click="editor.chain().focus().setTextAlign('center').run()" 
               :class="{ 'is-active': editor.isActive({ textAlign: 'center' }) }" 
               title="Выравнивание по центру"
               type="button">
            <i class="fa-solid fa-align-center"></i>
         </button>
         <button class="editorbutton" 
               @click="editor.chain().focus().setTextAlign('right').run()" 
               :class="{ 'is-active': editor.isActive({ textAlign: 'right' }) }" 
               title="Выравнивание по правому краю"
               type="button">
            <i class="fa-solid fa-align-right"></i>
         </button>
         <button class="editorbutton" 
               @click="editor.chain().focus().setTextAlign('justify').run()" 
               :class="{ 'is-active': editor.isActive({ textAlign: 'justify' }) }" 
               title="Выравнивание по ширине"
               type="button">
            <i class="fa-solid fa-align-justify"></i>
         </button>

         <button class="editorbutton" 
               @click="editor.chain().focus().toggleBulletList().run()" 
               :class="{ 'is-active': editor.isActive('bulletList') }" 
               title="Маркированный список"
               type="button">
            <i class="fa-solid fa-list-ul"></i>
         </button>
         <button class="editorbutton" 
               @click="editor.chain().focus().toggleOrderedList().run()" 
               :class="{ 'is-active': editor.isActive('orderedList') }" 
               title="Нумерованный список"
               type="button">
            <i class="fa-solid fa-list-ol"></i>
         </button>

         <button class="editorbutton" 
               @click="editor.chain().focus().toggleHeading({ level: 1 }).run()" 
               :class="{ 'is-active': editor.isActive('heading', { level: 1 }) }" 
               title="Заголовок 1"
               type="button">
            <i class="fa-solid fa-heading"></i> 1
         </button>
         <button class="editorbutton" 
               @click="editor.chain().focus().toggleHeading({ level: 2 }).run()" 
               :class="{ 'is-active': editor.isActive('heading', { level: 2 }) }" 
               title="Заголовок 2"
               type="button">
            <i class="fa-solid fa-heading"></i> 2
         </button>
         <button class="editorbutton" 
               @click="editor.chain().focus().toggleHeading({ level: 3 }).run()" 
               :class="{ 'is-active': editor.isActive('heading', { level: 3 }) }" 
               title="Заголовок 3"
               type="button">
            <i class="fa-solid fa-heading"></i> 3
         </button>

         <button class="editorbutton" 
               @click="editor.chain().focus().setHardBreak().run()" 
               title="Перенос строки"
               type="button">
            <i class="fa-solid fa-level-down-alt"></i>
         </button>
         <button class="editorbutton" 
               @click="editor.chain().focus().setParagraph().run()" 
               :class="{ 'is-active': editor.isActive('paragraph') }" 
               title="Абзац"
               type="button">
            <i class="fa-solid fa-paragraph"></i>
         </button>
         <button class="editorbutton" 
               @click="editor.chain().focus().setHorizontalRule().run()" 
               title="Горизонтальная линия"
               type="button">
            <i class="fa-solid fa-minus"></i>
         </button>

         <button type="button" class="editorbutton" @click="editor.chain().focus().insertTable({ rows: 3, cols: 3, withHeaderRow: true }).run()" title="Вставить таблицу">
            <i class="fa-solid fa-plus"></i> <i class="fa-solid fa-table"></i>
         </button>
         <!-- 
         <button type="button" class="editorbutton" @click="editor.chain().focus().insertContent(tableHTML, { parseOptions: { preserveWhitespace: false }}).run()" title="Вставить HTML таблицу">
            <i class="fa-solid fa-table"></i> HTML
         </button>
         -->
         <button type="button" class="editorbutton" @click="editor.chain().focus().deleteTable().run()" :disabled="!editor.can().deleteTable()" title="Удалить таблицу">
            <i class="fa-solid fa-table"></i> <i class="fa-regular fa-trash-can"></i>
         </button>

         <button type="button" class="editorbutton" @click="editor.chain().focus().addColumnBefore().run()" :disabled="!editor.can().addColumnBefore()" title="Добавить колонку перед">
            <i class="fa-solid fa-plus"></i> <i class="fa-solid fa-table-columns"></i> 
         </button>
         <button type="button" class="editorbutton" @click="editor.chain().focus().addColumnAfter().run()" :disabled="!editor.can().addColumnAfter()" title="Добавить колонку после">
            <i class="fa-solid fa-table-columns"></i> <i class="fa-solid fa-plus"></i>
         </button>
         <button type="button" class="editorbutton" @click="editor.chain().focus().deleteColumn().run()" :disabled="!editor.can().deleteColumn()" title="Удалить колонку">
            <i class="fa-solid fa-table-columns"></i> <i class="fa-regular fa-trash-can"></i>
         </button>

         <button type="button" class="editorbutton" @click="editor.chain().focus().addRowBefore().run()" :disabled="!editor.can().addRowBefore()" title="Добавить строку перед">
            <i class="fa-solid fa-plus"></i> <i class="fa-solid fa-table-cells-large"></i>
         </button>
         <button type="button" class="editorbutton" @click="editor.chain().focus().addRowAfter().run()" :disabled="!editor.can().addRowAfter()" title="Добавить строку после">
            <i class="fa-solid fa-table-cells-large"></i> <i class="fa-solid fa-plus"></i>
         </button>
         <button type="button" class="editorbutton" @click="editor.chain().focus().deleteRow().run()" :disabled="!editor.can().deleteRow()" title="Удалить строку">
            <i class="fa-solid fa-table-cells-large"></i> <i class="fa-regular fa-trash-can"></i> 
         </button>

         <button type="button" class="editorbutton" @click="editor.chain().focus().toggleHeaderColumn().run()" :disabled="!editor.can().toggleHeaderColumn()" title="Включить/выключить колонку заголовка">
            <i class="fa-solid fa-header"></i> <i class="fa-solid fa-table-columns"></i>
         </button>
         <button type="button" class="editorbutton" @click="editor.chain().focus().toggleHeaderRow().run()" :disabled="!editor.can().toggleHeaderRow()" title="Включить/выключить строку заголовка">
            <i class="fa-solid fa-header"></i> <i class="fa-solid fa-table-cells-large"></i>
         </button>
         <!-- 
         <button type="button" class="editorbutton" @click="editor.chain().focus().toggleHeaderCell().run()" :disabled="!editor.can().toggleHeaderCell()" title="Включить/выключить ячейку заголовка">
            <i class="fa-solid fa-header"></i> <i class="fa-solid fa-table-cells-large"></i>
         </button>
         -->

         <button type="button" class="editorbutton" @click="editor.chain().focus().mergeOrSplit().run()" :disabled="!editor.can().mergeOrSplit()" title="Объединить или разделить">
            <i class="fa-solid fa-compress-alt"></i> 
         </button>

         <!-- 
         <button type="button" class="editorbutton" @click="editor.chain().focus().setCellAttribute('backgroundColor', '#FAF594').run()" :disabled="!editor.can().setCellAttribute('backgroundColor', '#FAF594')" title="Установить атрибут ячейки">
            <i class="fa-solid fa-cogs"></i> 
         </button>

         <button type="button" class="editorbutton" @click="editor.chain().focus().fixTables().run()" :disabled="!editor.can().fixTables()" title="Исправить таблицы">
            <i class="fa-solid fa-sync-alt"></i> 
         </button>

         <button type="button" class="editorbutton" @click="editor.chain().focus().goToNextCell().run()" :disabled="!editor.can().goToNextCell()" title="Перейти к следующей ячейке">
            <i class="fa-solid fa-arrow-right"></i> 
         </button>

         <button type="button" class="editorbutton" @click="editor.chain().focus().goToPreviousCell().run()" :disabled="!editor.can().goToPreviousCell()" title="Перейти к предыдущей ячейке">
            <i class="fa-solid fa-arrow-left"></i> 
         </button>
         -->

         <button class="editorbutton"
               @click="editor.chain().focus().toggleBlockquote().run()" 
               :class="{ 'is-active': editor.isActive('blockquote') }" 
               title="Цитата"
               type="button">
            <i class="fa-solid fa-quote-left"></i>
         </button>
         <!-- 
         <button class="editorbutton"
               @click="editor.chain().focus().toggleCode().run()" 
               :disabled="!editor.can().chain().focus().toggleCode().run()" 
               :class="{ 'is-active': editor.isActive('code') }" 
               title="Вставить код"
               type="button">
            <i class="fa-solid fa-code"></i>
         </button>
         -->
         <button class="editorbutton"
               @click="editor.chain().focus().toggleCodeBlock().run()" 
               :class="{ 'is-active': editor.isActive('codeBlock') }" 
               title="Вставить блок кода"
               type="button">
               <i class="fa-solid fa-code"></i>
         </button>
         <!-- 
         <button class="editorbutton"
               @click="editor.chain().focus().clearNodes().run()" 
               title="Очистить узлы"
               type="button">
            <i class="fa-solid fa-trash"></i> Очистить узлы
         </button>
         -->
         <button class="editorbutton"
            @click="addLink()" title="Добавить ссылку" type="button">
            <i class="fa-solid fa-link"></i>
         </button>
         <button class="editorbutton"
            @click="addImage" title="Добавить картинку" type="button">
            <i class="fa-solid fa-image"></i>
         </button>


         <button class="editorbutton"
               @click="editor.chain().focus().undo().run()" 
               :disabled="!editor.can().chain().focus().undo().run()" 
               title="Отменить"
               type="button">
            <i class="fa-solid fa-undo"></i>
         </button>
         <button class="editorbutton"
               @click="editor.chain().focus().redo().run()" 
               :disabled="!editor.can().chain().focus().redo().run()" 
               title="Повторить"
               type="button">
            <i class="fa-solid fa-redo"></i>
         </button>

      </div>
      
      <editor-content :editor="editor" />

   </div>

</template>
 
<script>
import StarterKit from '@tiptap/starter-kit';
import Highlight from '@tiptap/extension-highlight';
import TextAlign from '@tiptap/extension-text-align';
import Underline from '@tiptap/extension-underline'
import Table from '@tiptap/extension-table';
import TableHeader from '@tiptap/extension-table-header';
import TableCell from '@tiptap/extension-table-cell';
import TableRow from '@tiptap/extension-table-row';
import Link from '@tiptap/extension-link';
import Image from '@tiptap/extension-image';
import Dropcursor from '@tiptap/extension-dropcursor';
import { Editor, EditorContent } from '@tiptap/vue-3';
import '@fortawesome/fontawesome-free/css/all.css';

const ImageWithStyle = Image.extend({
  addAttributes() {
    return {
      ...this.parent?.(),
      style: {
        default: '',
      },
    };
  },
});

export default {
  components: {
    EditorContent,
  },
  props: {
    modelValue: {
      type: String,
      default: '',
    },
  },
  data() {
    return {
      editor: null,
    };
  },
  mounted() {
    this.editor = new Editor({
      content: this.modelValue || "",
      extensions: [
        StarterKit,
        TextAlign.configure({
          types: ['heading', 'paragraph'],
        }),
        Underline,
        Highlight,
        Table.configure({
          resizable: true,
        }),
        TableHeader,
        TableCell,
        TableRow,
        Link,
        ImageWithStyle.configure({
          inline: true,
        }),
        Dropcursor,
      ],
    });
    this.$emit('update:modelValue', this.editor.getHTML());
    this.editor.on('update', () => {
      this.$emit('update:modelValue', this.editor.getHTML());
    });
  },
  beforeUnmount() {
    if (this.editor) {
      this.editor.destroy();
    }
  },
  methods: {
    addLink() {
      const url = prompt('Введите URL');
      if (url) {
        this.editor.chain().focus().setLink({ href: url }).run();
      }
    },
    addImage() {
      const url = prompt('Введите URL');
      const width = prompt('Введите ширину изображения в пикселях (например, 500)');
      if (url) {
        this.editor.chain().focus().setImage({
          src: url,
          style: `width: ${width}px`,
        }).run();
      }
    },
    getContent() {
      return this.editor?.getHTML() || '';
    },
    setContent(html) {
    this.editor?.chain().focus().setContent(html).run();
    },
    insertContent(html) {
    this.editor?.chain().focus().insertContent(html).run();
    },
    clearContent() {
      if (this.editor) {
        this.editor?.chain().focus().clearContent().run();
      }
    },
  },
};
</script>


